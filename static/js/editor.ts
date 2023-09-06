import { Markers } from "./markers";
import { EventEmitter } from "./event-emitter";
export type Breakpoints = Record<number, string>;
export enum EditorType {
  MAIN,
  MODAL,
  COMMON_MISTAKES,
  CHEATSHEET,
  PARSONS,
  EXAMPLE
}

type EditorEventEmitter = EventEmitter<EditorEvent>;
type OnEditorEventParameters = Parameters<EditorEventEmitter['on']>;

export interface EditorEvent {
  readonly change: string;
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
  setHighlighterForLevel(level: number): void;

  /**
   * Resizes the editor after changing its size programatically
   */
  resize(): void;

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
   * Returns the breakpoints as a map-to-css-class
   */
  getBreakpoints(): Breakpoints;
  /**
   * An event handler for the HedyEditor 
   * @param key the event
   * @param handler  the event handler function
   */
  on(key: OnEditorEventParameters[0], handler: OnEditorEventParameters[1]): void;
  
  markers: Markers;
}