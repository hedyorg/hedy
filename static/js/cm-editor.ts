import { HedyEditor, EditorType, Breakpoints, HedyEditorCreator } from "./editor";
import { Markers } from "./markers";
import { basicSetup } from 'codemirror';
import { EditorView } from '@codemirror/view'
import { Compartment, EditorState } from '@codemirror/state'
import { oneDark } from '@codemirror/theme-one-dark';

export class HedyCodeMirrorEditorCreator implements HedyEditorCreator {
    /**
     * This function should initialize the editor and set up all the required
     * event handlers
     * @param $editor reference to the div that contains the main editor
     * @param editorType the type of the editor
     * @param dir the direction of the text
     * @return {HedyEditor} The initialized Hedy editor instance
     */
    initializeEditorWithGutter($editor: JQuery, editorType: EditorType, dir: string = "ltr"): HedyCodeMirrorEditor {
        let editor: HedyCodeMirrorEditor = new HedyCodeMirrorEditor($editor.get(0)!, $editor.data('readonly'), editorType, dir);
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

        return new HedyCodeMirrorEditor(preview, true, editorType, dir);
    }
}

export class HedyCodeMirrorEditor implements HedyEditor {
    markers: Markers | undefined;
    private view: EditorView;
    private readMode = new Compartment; // Configuration for the editor read mode
    private theme = new Compartment;
    private themeStyles: Record<string, any>;
    
    constructor(element: HTMLElement, isReadOnly: boolean, editorType: EditorType, dir: string = "ltr") {
        console.log(element, isReadOnly, editorType, dir);
        
        this.themeStyles = {
            "&": {
                height: "352px", 
                background: '#272822', 
                fontSize: '15.2px', 
                color: 'white',
                borderRadius: '4px'
            },
            
            ".cm-scroller": {
                overflow: "auto"
            },

            ".cm-gutters": {
                borderRadius: '4px'
            },
        }
        
        const mainEditorStyling = EditorView.theme(this.themeStyles);
        
        const state = EditorState.create({
            doc: '',
            extensions: [
                basicSetup,
                oneDark,
                this.theme.of(mainEditorStyling),
                this.readMode.of(EditorState.readOnly.of(isReadOnly)),
            ]
        });
        this.view = new EditorView({
            parent: element,
            state: state
        });

    }

    /**
    * Set the highlither rules for a particular level
    * @param level      
    */
    setHighlighterForLevel(level: number): void {
        // pass
        console.log(level);
    }
    /**
    * @returns the string of the current program in the editor
    */
    public get contents(): string {
        return '';
    }

    /**
     * Sets the editor contents.
     * @param content the content that wants to be set in the editor
     */
    public set contents(content: string) {
        // pass
        console.log(content);
    }

    /**     
     * @returns if the editor is set to read-only mode
     */
    public get isReadOnly(): boolean {
        return false;
    }

    /**
     * Sets the read mode of the editor
     */
    public set isReadOnly(isReadMode: boolean) {
        // pass
        console.log(isReadMode)
    }

    /**
     * Resizes the editor after changing its size programatically
     */
    resize(newHeight?: number): void {
        if (newHeight === undefined) {
            console.log('Error! When resizing a CodeMirror instance, you need to provide the new height');
            return;
        }
        // Change the size of the container element of the editor
        // Via reconfiguring the editors theme
        this.themeStyles['&'].height = `${newHeight}px`;
               this.view.dispatch({
                effects: this.theme.reconfigure(EditorView.theme(this.themeStyles))
        });
    }

    /**
     * Focuses the text area for the current editor
     */
    focus(): void {
        this.view.focus();
    }

    /**
     * Clears the errors and annotations in the editor
     */
    clearErrors(): void {
        // pass
    }

    /**     
     * Moves to the cursor to the end of the current file
     */
    moveCursorToEndOfFile(): void {
        const endPos = this.view.state.doc.length;
        this.view.dispatch(
            this.view.state.update({ selection: {anchor: endPos, head: endPos}})
        );
    }

    /**
     * Clears the selected text
     */
    clearSelection(): void {
        // pass
    }

    /**
    * Removes all breakpoints on the rows.
    **/
    clearBreakpoints(): void {
        // pass
    }

    /**
     * If this editor is used as a main editor, we set the options here
     */
    configureMainEditor(): void {
        // pass
    }

    /**
   * The '@types/ace' package has the type of breakpoints incorrect
   *
   * It's actually a map of number-to-class. Class is usually 'ace_breakpoint'
   * but can be something you pick yourself.
   */
    getBreakpoints(): Breakpoints {
        return {} as Breakpoints;
    }

    getHighlighter(level: number): string {
        return `${level}`;
    }


    public on(key: any, handler: any) {
        console.log(key, handler)
    }

    public trimTrailingSpace() {
        // pass
    }

    public switchProgrammersMode(isProgrammersMode: boolean) {
        if (isProgrammersMode) {
            // Switch to programmers mode
            this.themeStyles['&'].height = "576px";
        } else {
            // Switch back to normal mode
            this.themeStyles['&'].height = "352px";
        }    
        this.view.dispatch({
            effects: this.theme.reconfigure(EditorView.theme(this.themeStyles))
        });
    }
}