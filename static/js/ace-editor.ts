import { theLocalSaveWarning } from "./app";
import { HedyEditorCreator, HedyEditor } from "./editor";
import { error } from "./modal";

export class HedyAceEditorCreator implements HedyEditorCreator {
  /**
   * This function should initialize the editor and set up all the required
   * event handlers
   * @param $editor reference to the div that contains the main editor
   */
  initializeMainEditor($editor: JQuery): HedyAceEditor | undefined {
    if (!$editor.length) return undefined;

    // Set const value to determine the current page direction -> useful for ace editor settings
    const dir = $("body").attr("dir");
    
    let mainEditor: HedyAceEditor = this.turnIntoEditor($editor.get(0)!, $editor.data('readonly'), true);        
    mainEditor.setShowPrintMargin(false);
    mainEditor.renderer.setScrollMargin(0, 0, 0, 20)
    mainEditor.addEventListener('change', () => {
      theLocalSaveWarning.setProgramLength(this.mainEditor!.getValue().split('\n').length);
    });
    error.setEditor(editor);
    markers = new Markers(theGlobalEditor);

    window.Range = ace.require('ace/range').Range // get reference to ace/range

    if (dir === "rtl") {
      editor.setOptions({ rtl: true });
    }

    // If prompt is shown and user enters text in the editor, hide the prompt.
    editor.on('change', function () {
      if (askPromptOpen) {
        stopit();
        editor.focus(); // Make sure the editor has focus, so we can continue typing
      }
      if ($('#ask-modal').is(':visible')) $('#inline-modal').hide();
      askPromptOpen = false;
      $('#runit').css('background-color', '');

      clearErrors(editor);
      //removing the debugging state when loading in the editor
      stopDebug();
    });

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
        editor.navigateFileEnd();
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

    // *** Debugger ***
    initializeDebugger({
      editor: theGlobalEditor,
      markers,
      level: theLevel,
      language: theLanguage,
    });

    return editor;
  }
  /**
   * 
   * @param element the element that will contain this editor
   * @param isReadOnly to decide weather to remove the cursor
   * @param isMainEditor should we show the line numbers
   */
  turnIntoEditor: (element: HTMLElement, isReadOnly: boolean, isMainEditor: boolean) => HedyEditor;

  /**
   * Ininitialize an editor that appears in a modal
   * @param $editor reference to the div that contains this editor
   */
  initializeModalEditor: ($editor: JQuery) => HedyEditor;

  /**
   * Set the highlither rules for a particular level
   * @param level      
   */
  setHighliterForLevel: (level: string) => void;

  /**
   * @returns the string of the current program in the editor
   */
  getValue: () => string;

  /**     
   * @returns if the editor is set to read-only mode
   */
  getReadOnly: () => boolean;

  /**
   * Sets the editor contents.
   * @param content the content that wants to be set in the editor
   */
  setValue: (content: string) => void;

  /**
   * Trim trailing whitespaces
   */
  trimTrailingSpace: (editor: HedyEditor) => void

  /**
   * Resizes the editor after changing its size programatically
   */
  resize: () => void;

  /**
   * Focuses the text area for the current editor
   */
  focus: () => void;

  /**
   * Clears the errors and annotations in the editor
   */
  clearErrors: () => void;

  /**     
   * Moves to the cursor to the end of the current file
   */
  moveCursorToEndOfFile: () => void;

  /**
   * Clears the selected text
   */
  clearSelection: () => void;

  /**
  * Removes all breakpoints on the rows.
  **/
  clearBreakpoints(): void;
}

export class HedyAceEditor implements HedyEditor {
    /**
   * Set the highlither rules for a particular level
   * @param level      
   */
    setHighliterForLevel: (level: string) => void;

    /**
     * @returns the string of the current program in the editor
     */
    getValue: () => string;
  
    /**     
     * @returns if the editor is set to read-only mode
     */
    isReadOnly: () => boolean;
  
    /**
     * Sets the editor contents.
     * @param content the content that wants to be set in the editor
     */
    setValue: (content: string) => void;
  
    /**
     * Trim trailing whitespaces
     */
    trimTrailingSpace: (editor: HedyEditor) => void
  
    /**
     * Resizes the editor after changing its size programatically
     */
    resize: () => void;
  
    /**
     * Focuses the text area for the current editor
     */
    focus: () => void;
  
    /**
     * Clears the errors and annotations in the editor
     */
    clearErrors: () => void;
  
    /**     
     * Moves to the cursor to the end of the current file
     */
    moveCursorToEndOfFile: () => void;
  
    /**
     * Clears the selected text
     */
    clearSelection: () => void;
  
    /**
    * Removes all breakpoints on the rows.
    **/
    clearBreakpoints(): void;
  
}

