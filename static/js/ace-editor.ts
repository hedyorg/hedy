import {  theLevel, theLanguage} from "./app";
import { HedyEditorCreator, HedyEditor, Breakpoints, EditorType, EditorEvent } from "./editor";
import { initializeDebugger } from "./debugging";
import { Markers } from "./markers";
import { EventEmitter } from "./event-emitter";
// const MOVE_CURSOR_TO_BEGIN = -1;
const MOVE_CURSOR_TO_END = 1;
export class HedyAceEditorCreator implements HedyEditorCreator {
  /**
   * This function should initialize the editor and set up all the required
   * event handlers
   * @param $editor reference to the div that contains the main editor
   * @param editorType the type of the editor
   * @param dir the direction of the text
   * @return {HedyEditor} The initialized Hedy editor instance
   */
  initializeEditorWithGutter($editor: JQuery, editorType: EditorType, dir: string = "ltr"): HedyAceEditor {
    let editor: HedyAceEditor = new HedyAceEditor($editor.get(0)!, $editor.data('readonly'), editorType, dir);
    return editor;
  }
  /**
   * Initializes a read only editor
   *
   * @param {HTMLElement} preview - The element to preview the editor.
   * @return {HedyEditor} The initialized Hedy editor instance.
   */
  initializeReadOnlyEditor(preview: HTMLElement, dir: string = "ltr"): HedyEditor {
    let editorType: EditorType;
  
    if ($(preview).hasClass('common-mistakes')) {
      editorType = EditorType.COMMON_MISTAKES;
    } else if ($(preview).hasClass('cheatsheet')) {
      editorType = EditorType.CHEATSHEET;
    } else if ($(preview).hasClass('parsons')) {
      editorType = EditorType.PARSONS;
    } else {
      editorType = EditorType.EXAMPLE;
    }

    return new HedyAceEditor(preview, true, editorType, dir);
  }
}
  
export class HedyAceEditor implements HedyEditor {
  private _editor: AceAjax.Editor;
  private _markers?: Markers
  isReadOnly: boolean;
  private editorEvent = new EventEmitter<EditorEvent>({change: true});
  
  /**
   * 
   * @param {HTMLElement} element the element that will contain this editor
   * @param {boolean} isReadOnly to decide weather to remove the cursor
   * @param {EditorType} editorType the type of the editor, could be a main editor, a parsons editor, etc.
   * @param {string} dir the direction of the text
   */
  constructor(element: HTMLElement, isReadOnly: boolean, editorType: EditorType, dir: string = "ltr") {
    this._editor = ace.edit(element);
    this.isReadOnly = isReadOnly;
    this._editor.setTheme("ace/theme/monokai");
      
    if (isReadOnly) {
      this._editor.setValue(this._editor.getValue().trimRight(), -1);
      // Remove the cursor
      // Telling TS to ignore this line, because $cursorLayer is not correctly include in ace types
      // but it's there
      // @ts-ignore
      this._editor.renderer.$cursorLayer.element.style.display = "none";
      this._editor.setOptions({
        readOnly: true,
        showGutter: false,
        showPrintMargin: false,
        highlightActiveLine: false
      });
      // A bit of margin looks better
      this._editor.renderer.setScrollMargin(3, 3, 10, 20)

      // When it is the main editor -> we want to show line numbers!
      if (editorType === EditorType.MAIN) {
        this._editor.setOptions({
          showGutter: true
        });
      } else { // It's an example editor
         // Fits to content size
        this._editor.setOptions({ maxLines: Infinity });     
        if(editorType === EditorType.CHEATSHEET) {
          this._editor.setOptions({ minLines: 1 });
        } else if(editorType === EditorType.COMMON_MISTAKES) {
          this._editor.setOptions({
            showGutter: true,
            showPrintMargin: true,
            highlightActiveLine: true,
            minLines: 5,
          });
        } else if(editorType === EditorType.PARSONS) {
          this._editor.setOptions({
            minLines: 1,
            showGutter: false,
            showPrintMargin: false,
            highlightActiveLine: false
          });
        } else if(editorType === EditorType.EXAMPLE) {
          this._editor.setOptions({ minLines: 2 });
        }
      }
    } else {
      if (editorType === EditorType.MAIN) {
        this._editor.setShowPrintMargin(false);
        this._editor.renderer.setScrollMargin(0, 0, 0, 20);
        this.configureMainEditor();
      }
    }
    
    // Everything turns into 'ace/mode/levelX', except what's in    
    if (theLevel) {
      this.setHighlighterForLevel(theLevel)
    }

    if (dir === "rtl") {
      this._editor.setOptions({ rtl: true });
    }
  }
  
  /**
  * Set the highlither rules for a particular level
  * @param level      
  */
  setHighlighterForLevel(level: number): void { 
    const mode = this.getHighlighter(level);
    this._editor.session.setMode(mode);
  }

  /**
   * @returns the string of the current program in the editor
   */
  public get contents(): string { 
    // Always trim trailing whitespaces before returning the contents
    try {
      // This module may or may not exist, so let's be extra careful here.
      const whitespace = ace.require("ace/ext/whitespace");
      whitespace.trimTrailingSpace(this._editor.session, true);
    } catch (e) {
      console.error(e);
    }
    return this._editor.getValue();
  }

  /**
   * Sets the editor contents.
   * @param content the content that wants to be set in the editor
   */
  public set contents(content: string) {
    this._editor.setValue(content, MOVE_CURSOR_TO_END);
  }

  /**     
   * @returns if the editor is set to read-only mode
   */
  public get getIsReadOnly(): boolean {
    return this.isReadOnly;
  }
  
  /**
   * Sets the read mode of the editor
   */
  public set setIsreadOnly(isReadMode: boolean) {
    this._editor.setReadOnly(isReadMode);
    this.isReadOnly = isReadMode;
  }

  /**
   * Resizes the editor after changing its size programatically
   */
  resize(): void {
    this._editor.resize()
  }

  /**
   * Focuses the text area for the current editor
   */
  focus(): void { 
    this._editor.focus();
  }

  /**
   * Clears the errors and annotations in the editor
   */
  clearErrors(): void {
    // Not sure if we use annotations everywhere, but this was
    // here already.
    this._editor.session.clearAnnotations();
    this.markers?.clearErrors();
  }

  /**     
   * Moves to the cursor to the end of the current file
   */
  moveCursorToEndOfFile(): void { 
    this._editor.navigateFileEnd();
  }

  /**
   * Clears the selected text
   */
  clearSelection(): void {
    this._editor.clearSelection();
  }

  /**
  * Removes all breakpoints on the rows.
  **/
  clearBreakpoints(): void { 
    this._editor.session.clearBreakpoints();
  }

  /**
   * If this editor is used as a main editor, we set the options here
   */
  configureMainEditor(): void {
    this._markers = new Markers(this._editor);
    // *** Debugger *** //
    // TODO: FIX THIS
    initializeDebugger({
      editor: this._editor,
      markers: this.markers,
      level: theLevel,
      language: theLanguage,
    });
  }

  /**
 * The '@types/ace' package has the type of breakpoints incorrect
 *
 * It's actually a map of number-to-class. Class is usually 'ace_breakpoint'
 * but can be something you pick yourself.
 */
  getBreakpoints(): Breakpoints {
    return this._editor.session.getBreakpoints() as unknown as Breakpoints;
  }

  getHighlighter(level: number): string {
    return `ace/mode/level${level}`;
  }

  get markers(): Markers {
    return this._markers!;
  }

  public on(key: Parameters<typeof this.editorEvent.on>[0], handler: Parameters<typeof this.editorEvent.on>[1]) {
    const ret = this.editorEvent.on(key, handler);    
    this._editor.addEventListener(key, handler);
    return ret;
  }
}