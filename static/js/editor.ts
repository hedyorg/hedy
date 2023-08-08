import { Markers } from "./markers";

export type Breakpoints = Record<number, string>;


export interface HedyEditorCreator {
  // TODO: Not sure yet if it should return a HedyEditor or change local variable names
  /**
   * This function should initialize the editor and set up all the required
   * event handlers
   * @param $editor reference to the div that contains the main editor
   */
  initializeMainEditor: ($editor: JQuery) => HedyEditor | undefined;
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
}

export interface HedyEditor {
  /**
 * Represents whether there's an open 'ask' prompt
 */
  askPromptOpen: boolean;
  /**
   * Set the highlither rules for a particular level
   * @param level      
   */
  setHighliterForLevel: (level: number) => void;

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
  trimTrailingSpace: () => void

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
  clearBreakpoints: ()  => void;

  /**
   * Sets the main editor and also its options
   */
  configureMainEditor(): void;

  /**
   * Returns the breakpoints as a map-to-css-class
   */
  getBreakpoints: () => Breakpoints;

  /**
   * Sets the mode of the editor to read-only or editable depending
   * on the paramater
   * @param isReadMode whether the editor will be set to read only mode or not
   */
  setEditorMode: (isReadMode: boolean) => void;
  
  markers: Markers;
}