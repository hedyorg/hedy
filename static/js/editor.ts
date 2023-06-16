export interface HedyEditor {
    // TODO: Not sure yet if it should return a HedyEditor or change local variable names
    /**
     * This function should initialize the editor and set up all the required
     * event handlers
     * @param $editor reference to the div that contains the main editor
     */
    initializeMainEditor: ($editor: JQuery) => HedyEditor;
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
    initializeModalEditor: ($editor: JQuery)=> HedyEditor;

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
}