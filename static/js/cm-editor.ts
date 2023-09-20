import { HedyEditor, EditorType, Breakpoints, HedyEditorCreator, EditorEvent } from "./editor";
import { basicSetup } from 'codemirror';
import { Decoration, DecorationSet, EditorView, ViewUpdate } from '@codemirror/view'
import { EditorState, Compartment, StateEffect, StateField } from '@codemirror/state'
import { oneDark } from '@codemirror/theme-one-dark';
import { EventEmitter } from "./event-emitter";
import { deleteTrailingWhitespace } from '@codemirror/commands'


const addErrorLine = StateEffect.define<{row: number, col?: number}>()
  
const errorLineField = StateField.define<DecorationSet>({
    create() {
      return Decoration.none
    },
    update(errors, tr) {
      errors = errors.map(tr.changes)
      for (let e of tr.effects) if (e.is(addErrorLine)) {
        // Get line given the row number
        const line = tr.state.doc.line(e.value.row);
        errors = errors.update({
          add: [errorHighlightMark.range(line.from, line.from)]
        })
      }
      return errors
    },
    provide: f => EditorView.decorations.from(f)
})
  
const errorHighlightMark = Decoration.line({class: "cm-error-line"})

const errorHighlightTheme = EditorView.baseTheme({
    ".cm-error-line": {
        borderBottomWidth: "2px",
        borderTopWidth: "2px",        
        borderColor: "#F56565",
        backgroundColor: "#4299E1",
        opacity: 0.7
    }
})

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
    private view: EditorView;
    private readMode = new Compartment; // Configuration for the editor read mode
    private theme = new Compartment;
    private themeStyles: Record<string, any>;
    private editorEvent = new EventEmitter<EditorEvent>({
        change: true,
        guttermousedown: true,
        changeBreakpoint: true
      });

    constructor(element: HTMLElement, isReadOnly: boolean, editorType: EditorType, dir: string = "ltr") {
        console.log(editorType, dir);

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
                errorLineField,
                errorHighlightTheme
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
        return this.view.state.doc.toString();
    }

    /**
     * Sets the editor contents.
     * @param content the content that wants to be set in the editor
     */
    public set contents(content: string) {
        let transaction = this.view.state.update({ changes: { from: 0, to: this.view.state.doc.length, insert: content } });
        this.view.dispatch(transaction);
    }

    /**     
     * @returns if the editor is set to read-only mode
     */
    public get isReadOnly(): boolean {
        return this.view.state.readOnly;
    }

    /**
     * Sets the read mode of the editor
     */
    public set isReadOnly(isReadMode: boolean) {
        this.view.dispatch({
            effects: this.readMode.reconfigure(EditorState.readOnly.of(isReadMode))
        });
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
            this.view.state.update({ selection: { anchor: endPos } })
        );
    }

    /**
     * Clears the selected text leaving the anchor in its current position
     */
    clearSelection(): void {
        const currentSelection = this.view.state.selection;
        const currentAnchor = currentSelection.ranges[0].anchor;
        this.view.dispatch(this.view.state.update({ selection: { anchor: currentAnchor } }));
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

    public trimTrailingSpace() {
        deleteTrailingWhitespace(this.view);
    }

    public on(key: Parameters<typeof this.editorEvent.on>[0], handler: any) {
        // This type of handler works for when the view is updated
        // If in the future we need to add another type of handler to the editor
        // that hooks to the DOM, We can use the domEventHandlers configuration for that
        if (key === 'change') {
            const transaction = this.view.state.update({
                effects: StateEffect.appendConfig.of(EditorView.updateListener.of((v: ViewUpdate) => {                
                    if (v.docChanged) {
                        handler();
                    }
                }))
            })
            this.view.dispatch(transaction);
        }
    }

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
    highlightError(row: number, col?: number) {
        let effects: StateEffect<{row: number, col?: number}>[] = [addErrorLine.of({row, col})]
        this.view.dispatch({effects})
    }

    /**
     * Remove all incorrect lines markers
     */
    // clearIncorrectLines(): void => for Skip Faulty

    /**
     * Set the current line in the debugger
     */
    setDebuggerCurrentLine(line: number | undefined) {
        // pass
        console.log(line);
    }

    /**
     * Mark the given set of lines as currently struck through
     */
    strikethroughLines(lines: number[]) {
        // pass
        console.log(lines);
    }
}