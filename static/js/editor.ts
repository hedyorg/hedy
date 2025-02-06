import { EventEmitter } from "./event-emitter";
export type Breakpoints = Record<number, string>;
export enum EditorType {
  MAIN,
  MODAL,
  COMMON_MISTAKES,
  CHEATSHEET,
  PARSONS,
  EXAMPLE,
  WORKBOOK
}

type EditorEventEmitter = EventEmitter<EditorEvent>;
type OnEditorEventParameters = Parameters<EditorEventEmitter['on']>;

export interface SourceRange {
  readonly startLine: number;
  readonly startColumn: number;
  readonly endLine: number;
  readonly endColumn: number;
}

export interface EditorEvent {
  readonly change: string;
  readonly guttermousedown: string;
  readonly changeBreakpoint: string;
  readonly click: string
}

export interface HedyEditorCreator {
  /**
   * This function should initialize the editor and set up all the required
   * event handlers
   * @param {JQuery} $editor reference to the div that contains the main editor
   * @param {EditorType} editorType the type of the editor
   */
  initializeEditorWithGutter($editor: JQuery, editorType: EditorType, dir?: string): HedyEditor;

  /**
   * Initializes a read only editor
   *
   * @param {HTMLElement} preview - The element to preview the editor.
   * @return {HedyEditor} The initialized Hedy editor instance.
   */
  initializeReadOnlyEditor(preview: HTMLElement, dir?: string): HedyEditor;
}

export interface HedyEditor {
  /**
   * The contents of the editor
   */
  contents: string;
  /**
   * if the editor is set to read-only mode
   */
  isReadOnly: boolean;
  /**
   * Set the highlither rules for a particular level
   * @param level
   */
  setHighlighterForLevel(level: number, keywordLang: string): void;

  /**
   * Resizes the editor after changing its size programatically
   * @param newHeight the new height of the editor in rem, if supplied
   */
  resize(newHeight?: number): void;

  /**
   * Focuses the text area for the current editor
   */
  focus(): void;

  /**
   * Clears the errors and annotations in the editor
   */
  clearErrors(): void;

  /**
   * Moves to the cursor to the end of the current file
   */
  moveCursorToEndOfFile(): void;

  /**
   * Clears the selected text
   */
  clearSelection(): void;

  /**
  * Removes all breakpoints on the rows.
  **/
  clearBreakpoints(): void;

  /**
   * An event handler for the HedyEditor
   * @param key the event
   * @param handler  the event handler function
   */

  on(key: OnEditorEventParameters[0], handler: any): void;

  /**
   * Trim trailing whitespaces
   */
  trimTrailingSpace: () => void;

  /**
   * Mark an error location in the editor
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
  highlightError(row: number, col?: number): void;

  /**
   * set incorrect line
   */
  setIncorrectLine(range: SourceRange, lineIndex: number): void;

  /**
   * Remove all incorrect lines markers
   */
  clearIncorrectLines(): void;

  /**
   * Set the current line in the debugger
   */
  setDebuggerCurrentLine(line?: number, startPos?: number, finishPos?: number): void;

  /**
   * Mark the given set of lines as currently struck through
   */
  getActiveContents(debugLine?: string | null): string;

  /**
   * Skip faulty event handler
   */
  skipFaultyHandler(event?: MouseEvent): void;
}
