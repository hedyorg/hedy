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
     * @returns 
     */   
    initializeModalEditor: ($editor: JQuery)=> HedyEditor;

    /**
     * Set the highlither rules for a particular level
     * @param level 
     * @returns 
     */
    setHighliterForLevel: (level: string) => void;
    
    /**
     * Returns the string of the current program in the editor
     */
    getContent: () => string
}