import { theLevel } from "./app";
import { HedyEditorCreator, HedyEditor, Breakpoints, EditorType, EditorEvent, SourceRange } from "./editor";
import { EventEmitter } from "./event-emitter";
// const MOVE_CURSOR_TO_BEGIN = -1;
const MOVE_CURSOR_TO_END = 1;

/**
 * The 'ace_breakpoint' style has been overridden to show a sleeping emoji in the gutter
 */
const BP_DISABLED_LINE = 'ace_breakpoint';

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
  private editorEvent = new EventEmitter<EditorEvent>({
    change: true,
    guttermousedown: true,
    changeBreakpoint: true,
    click: true
  });
  private markerClasses = new Map<number, string>();
  private currentLineMarker?: MarkerLocation;
  // Map line numbers to markers
  private strikeMarkers = new Map<number, number>();

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
        // only show gutter when its the main editor
        readOnly: editorType === EditorType.MAIN,
        showGutter: false,
        showPrintMargin: false,
        highlightActiveLine: false
      });
      // A bit of margin looks better
      this._editor.renderer.setScrollMargin(3, 3, 10, 20)

      // It's an example editor
      // Fits to content size
      this._editor.setOptions({ maxLines: Infinity });
      if (editorType === EditorType.CHEATSHEET) {
        this._editor.setOptions({ minLines: 1 });
      } else if (editorType === EditorType.COMMON_MISTAKES) {
        this._editor.setOptions({
          showGutter: true,
          showPrintMargin: true,
          highlightActiveLine: true,
          minLines: 5,
        });
      } else if (editorType === EditorType.PARSONS) {
        this._editor.setOptions({
          minLines: 1,
          showGutter: false,
          showPrintMargin: false,
          highlightActiveLine: false
        });
      } else if (editorType === EditorType.EXAMPLE) {
        this._editor.setOptions({ minLines: 2 });
      }
    } else {
      if (editorType === EditorType.MAIN) {
        this._editor.setShowPrintMargin(false);
        this._editor.renderer.setScrollMargin(0, 0, 0, 20);
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
  public get isReadOnly(): boolean {
    return this._editor.getReadOnly();
  }

  /**
   * Sets the read mode of the editor
   */
  public set isReadOnly(isReadMode: boolean) {
    this._editor.setReadOnly(isReadMode);
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
    for (const marker of this.findMarkers('editor-error')) {
      this.removeMarker(marker);
    }
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
 * The '@types/ace' package has the type of breakpoints incorrect
 *
 * It's actually a map of number-to-class. Class is usually 'ace_breakpoint'
 * but can be something you pick yourself.
 */
  getDeactivatedLines(): Breakpoints {
    return this._editor.session.getBreakpoints() as unknown as Breakpoints;
  }

  getHighlighter(level: number): string {
    return `ace/mode/level${level}`;
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

  public on(key: Parameters<typeof this.editorEvent.on>[0], handler: any) {
    const ret = this.editorEvent.on(key, handler);
    // This particular event needs to be attached to the session
    if (key == 'changeBreakpoint'){
      this._editor.session.on(key, handler);
    } else {
      this._editor.addEventListener(key, handler);
    }
    return ret;
  }

  /**
   * Mark an error location in the ace editor
   *
   * The error occurs at the given row, and optionally has a column and
   * and a length.
   *
   * If 'col' is not given, the entire line will be highlighted red. Otherwise
   * the character at 'col' will be highlighted, optionally extending for
   * 'length' characters.
   *
   * 'row' and 'col' are 1-based.
   */
  public highlightError(row: number, col?: number) {
    // Set a marker on the error spot, either a fullLine or a text
    // class defines the related css class for styling; which is fixed in styles.css with Tailwind
    if (col === undefined) {
      // If the is no column, highlight the whole row
      this.addMarker(
        new ace.Range(row - 1, 1, row - 1, 2),
        "editor-error", "fullLine"
      );
      return;
    }
    // If we get here we know there is a column -> dynamically get the length of the error string
    // As we assume the error is supposed to target a specific word we get row[column, whitespace].
    const length = this._editor.session.getLine(row - 1).slice(col - 1).split(/(\s+)/)[0].length;
    if (length > 0) {
      // If there is a column, only highlight the relevant text
      this.addMarker(new ace.Range(row - 1, col - 1, row - 1, col - 1 + length),
        "editor-error", "text"
      );
    } else {
      // If we can't find the word to highlight, highlight the whole line
      this.addMarker(
        new ace.Range(row - 1, 1, row - 1, 2),
        "editor-error", "fullLine"
      );
    }
  }


  /**
   * Set incorrect line marker
   */
  public setIncorrectLine(range: SourceRange, lineIndex: number){
    // Positions in Ace are 0-based
    const aceRange = new ace.Range(
      range.startLine - 1, range.startColumn - 1,
      range.endLine - 1, range.endColumn - 1
    );

    this.addMarker(aceRange, `ace_incorrect_hedy_code_${lineIndex}`, "text", true);
  }

  /**
   * Remove all incorrect lines
   */
  public clearIncorrectLines() {
    const markers = this._editor.session.getMarkers(true);

    if (markers) {
      for (const index in markers) {
        let marker = markers[index];
        if (marker.clazz.includes('ace_incorrect_hedy_code')){
          this.removeMarker(Number(index));
        }
      }
    }
  }

  /**
   * Set the current line in the debugger
   */
  public setDebuggerCurrentLine(line: number | undefined) {
    if (this.currentLineMarker?.line === line) {
      return;
    }

    if (this.currentLineMarker) {
      this.removeMarker(this.currentLineMarker.id);
    }

    if (line === undefined) {
      this.currentLineMarker = undefined;
      return;
    }

    const id = this.addMarker(new ace.Range(line, 0, line, 999), 'debugger-current-line', 'fullLine');
    this.currentLineMarker = { line, id };
  }

  /**
   * Mark the given set of lines as currently struck through
   */
  public strikethroughLines(lines: number[]) {
    const struckLines = new Set(lines);

    // First remove all markers that are no longer in the target set
    const noLongerStruck = Array.from(this.strikeMarkers.entries())
      .filter(([line, _]) => !struckLines.has(line))
    for (const [line, id] of noLongerStruck) {
      this.removeMarker(id);
      this.strikeMarkers.delete(line);
    }

    // Then add markers for lines need to be struck
    const newlyStruck = lines
      .filter(line => !this.strikeMarkers.has(line));
    for (const line of newlyStruck) {
      const id = this.addMarker(new ace.Range(line, 0, line, 999), 'disabled-line', 'text', true);
      this.strikeMarkers.set(line, id);
    }
  }

  /**
   * Add a marker and remember the class
   */
  private addMarker(range: AceAjax.Range, klass: string, scope: 'text' | 'line' | 'fullLine', inFront = false) {
    const id = this._editor.session.addMarker(range, klass, scope, inFront);
    this.markerClasses.set(id, klass);
    return id;
  }

  private removeMarker(id: number) {
    this._editor.session.removeMarker(id);
    this.markerClasses.delete(id);
  }

  private findMarkers(klass: string) {
    return Array.from(this.markerClasses.entries())
      .filter(([_, k]) => k === klass)
      .map(([id, _]) => id);
  }
  public getActiveContents(debugLine: string | null): string {
    let code = this._editor.session.getValue();
    const breakpoints = this.getDeactivatedLines();
    
    if (code) {
      let lines = code.split('\n');
      if(debugLine != null){
        lines = lines.slice(0, parseInt(debugLine) + 1);
      }
      for (let i = 0; i < lines.length; i++) {
        if (breakpoints[i] == BP_DISABLED_LINE) {
          lines[i] = '';
        }
      }
      code = lines.join('\n');
    }
  
    return code;
  }
}


interface MarkerLocation {
  readonly line: number;
  readonly id: number;
}
