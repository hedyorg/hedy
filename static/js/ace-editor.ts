import { theLocalSaveWarning, theLevel, runit, stopit, theLanguage, triggerAutomaticSave } from "./app";
import { HedyEditorCreator, HedyEditor, Breakpoints } from "./editor";
import { error } from "./modal";
import { initializeDebugger, stopDebug } from "./debugging";
import { Markers } from "./markers";

// const MOVE_CURSOR_TO_BEGIN = -1;
const MOVE_CURSOR_TO_END = 1;
export class HedyAceEditorCreator implements HedyEditorCreator {
  /**
   * This function should initialize the editor and set up all the required
   * event handlers
   * @param $editor reference to the div that contains the main editor
   */
  initializeMainEditor($editor: JQuery): HedyAceEditor {
    let editor: HedyAceEditor = this.turnIntoEditor($editor.get(0)!, $editor.data('readonly'), true);
    editor.configureMainEditor();
    error.setEditor(editor);
    window.Range = ace.require('ace/range').Range // get reference to ace/range

    // *** KEYBOARD SHORTCUTS ***
    let altPressed: boolean | undefined;
    // alt is 18, enter is 13
    window.addEventListener('keydown', function (ev) {
      const keyCode = ev.keyCode;
      if (keyCode === 18) {
        altPressed = true;
        return;
      }
      if (keyCode === 13 && altPressed) {
        if (!theLevel || !theLanguage) {
          throw new Error('Oh no');
        }
        runit(theLevel, theLanguage, "", function () {
          $('#output').focus();
        });
      }
      // We don't use jquery because it doesn't return true for this equality check.
      if (keyCode === 37 && document.activeElement === document.getElementById('output')) {
        editor.focus();
        editor.moveCursorToEndOfFile();
      }
    });

    window.addEventListener('keyup', function (ev) {
      triggerAutomaticSave();
      const keyCode = ev.keyCode;
      if (keyCode === 18) {
        altPressed = false;
        return;
      }
    });

    return editor;
  }
  /**
   * 
   * @param element the element that will contain this editor
   * @param isReadOnly to decide weather to remove the cursor
   * @param isMainEditor should we show the line numbers
   */
  turnIntoEditor(element: HTMLElement, isReadOnly: boolean, isMainEditor = false): HedyAceEditor {
    let hedyEditor: HedyAceEditor = new HedyAceEditor();
    const editor = ace.edit(element);
    editor.setTheme("ace/theme/monokai");
    if (isReadOnly) {
      editor.setValue(editor.getValue().trimRight(), -1);
      // Remove the cursor
      editor.renderer.$cursorLayer.element.style.display = "none";
      editor.setOptions({
        readOnly: true,
        showGutter: false,
        showPrintMargin: false,
        highlightActiveLine: false
      });
      // A bit of margin looks better
      editor.renderer.setScrollMargin(3, 3, 10, 20)

      // When it is the main editor -> we want to show line numbers!
      if (isMainEditor) {
        editor.setOptions({
          showGutter: true
        });
      }
    }
    
    hedyEditor.editor = editor;    
    // Everything turns into 'ace/mode/levelX', except what's in    
    if (theLevel) {
      hedyEditor.setHighliterForLevel(theLevel)
    }
    return hedyEditor;
  }

  /**
   * Ininitialize an editor that appears in a modal
   * @param $editor reference to the div that contains this editor
   */
  initializeModalEditor($editor: JQuery): HedyEditor {
    let editor = this.turnIntoEditor($editor.get(0)!, true);
    error.setEditor(editor);
    window.Range = ace.require('ace/range').Range // get reference to ace/range

  // *** KEYBOARD SHORTCUTS ***

  let altPressed: boolean | undefined;

  // alt is 18, enter is 13
  window.addEventListener ('keydown', function (ev) {
    const keyCode = ev.keyCode;
    if (keyCode === 18) {
      altPressed = true;
      return;
    }
    if (keyCode === 13 && altPressed) {
      runit (theLevel, theLanguage, "", function () {
        $ ('#output').focus ();
      });
    }
    // We don't use jquery because it doesn't return true for this equality check.
    if (keyCode === 37 && document.activeElement === document.getElementById ('output')) {
      editor.focus();
      editor.moveCursorToEndOfFile();
    }
  });
  window.addEventListener ('keyup', function (ev) {
    const keyCode = ev.keyCode;
    if (keyCode === 18) {
      altPressed = false;
      return;
    }
  });
    return editor;
  }

  initializeExampleEditor(preview: HTMLElement): HedyEditor {
    const dir = $("body").attr("dir");
    const exampleEditor = this.turnIntoEditor(preview, true);
    // Fits to content size
    exampleEditor.setOptions({ maxLines: Infinity });
    if ($(preview).hasClass('common-mistakes')) {
      exampleEditor.setOptions({
        showGutter: true,
        showPrintMargin: true,
        highlightActiveLine: true,
        minLines: 5,
      });
    } else if ($(preview).hasClass('cheatsheet')) {
      exampleEditor.setOptions({ minLines: 1 });
    } else if ($(preview).hasClass('parsons')) {
      exampleEditor.setOptions({
        minLines: 1,
        showGutter: false,
        showPrintMargin: false,
        highlightActiveLine: false
      });
    } else {
      exampleEditor.setOptions({ minLines: 2 });
    }

    if (dir === "rtl") {
        exampleEditor.setOptions({ rtl: true });
    }
    return exampleEditor;
  }
}

export class HedyAceEditor implements HedyEditor {
  private _editor?: AceAjax.Editor;
  private _markers?: Markers
  askPromptOpen: boolean = false;

  /**
 * Set the highlither rules for a particular level
 * @param level      
 */
  setHighliterForLevel(level: number): void { 
    const mode = this.getHighlighter(level);
    this._editor?.session.setMode(mode);
  }

  /**
   * @returns the string of the current program in the editor
   */
  getValue(): string { 
    return this._editor!.getValue();
  }

  /**     
   * @returns if the editor is set to read-only mode
   */
  isReadOnly(): boolean {
    return this._editor!.getReadOnly();
  }

  /**
   * Sets the editor contents.
   * @param content the content that wants to be set in the editor
   */
  setValue(content: string): void {
    this._editor?.setValue(content, MOVE_CURSOR_TO_END);
  }

  /**
   * Trim trailing whitespaces
   */
  trimTrailingSpace(): void {
    try {
      // This module may or may not exist, so let's be extra careful here.
      const whitespace = ace.require("ace/ext/whitespace");
      whitespace.trimTrailingSpace(this._editor!.session, true);
    } catch (e) {
      console.error(e);
    }
  }

  /**
   * Resizes the editor after changing its size programatically
   */
  resize(): void {
    this._editor?.resize()
  }

  /**
   * Focuses the text area for the current editor
   */
  focus(): void { 
    this._editor?.focus();
  }

  /**
   * Clears the errors and annotations in the editor
   */
  clearErrors(): void {
    // Not sure if we use annotations everywhere, but this was
    // here already.
    this._editor?.session.clearAnnotations();
    this.markers?.clearErrors();
  }

  /**     
   * Moves to the cursor to the end of the current file
   */
  moveCursorToEndOfFile(): void { 
    this._editor?.navigateFileEnd();
  }

  /**
   * Clears the selected text
   */
  clearSelection(): void {
    this._editor?.clearSelection();
  }

  /**
  * Removes all breakpoints on the rows.
  **/
  clearBreakpoints(): void { 
    this._editor?.session.clearBreakpoints();
  }

  /**
   * If this editor is used as a main editor, we set the options here
   */
  configureMainEditor(): void {
    this._editor?.setShowPrintMargin(false);
    this._editor?.renderer.setScrollMargin(0, 0, 0, 20)
    this._editor?.addEventListener('change', () => {
      theLocalSaveWarning.setProgramLength(this._editor!.getValue().split('\n').length);
    });
    // Set const value to determine the current page direction -> useful for ace editor settings
    const dir = $("body").attr("dir");
    if (dir === "rtl") {
      this._editor?.setOptions({ rtl: true });
    }

    // If prompt is shown and user enters text in the editor, hide the prompt.
    this._editor?.on('change', () => {
      if (this.askPromptOpen) {
        stopit();
        this._editor?.focus(); // Make sure the editor has focus, so we can continue typing
      }
      if ($('#ask-modal').is(':visible')) $('#inline-modal').hide();
      this.askPromptOpen = false;
      $('#runit').css('background-color', '');
      this.clearErrors();
      //removing the debugging state when loading in the editor
      stopDebug();
    });

    this._markers = new Markers(this._editor!);

          // *** Debugger *** //
      // TODO: FIX THIS
      initializeDebugger({
        editor: this._editor!,
        markers: this.markers,
        level: theLevel,
        language: theLanguage,
      });
  }

  set editor(editor: AceAjax.Editor) {
    this._editor = editor;
  }

  /**
 * The '@types/ace' package has the type of breakpoints incorrect
 *
 * It's actually a map of number-to-class. Class is usually 'ace_breakpoint'
 * but can be something you pick yourself.
 */
  getBreakpoints(): Breakpoints {
    return this._editor?.session.getBreakpoints() as unknown as Breakpoints;
  }

  setEditorMode(isReadMode: boolean): void {
    this._editor?.setReadOnly(isReadMode);
  }

  getHighlighter(level: number): string {
    return `ace/mode/level${level}`;
  }

  setOptions(options: object) {
    this._editor?.setOptions(options);
  }

  get editor(): AceAjax.Editor {
    return this._editor!;
  }

  get markers(): Markers {
    return this._markers!;
  }
}

