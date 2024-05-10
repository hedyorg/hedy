import { HedyEditor, EditorType, HedyEditorCreator, EditorEvent, SourceRange } from "./editor";
import { EditorView, ViewUpdate, drawSelection, dropCursor, highlightActiveLine,
        highlightActiveLineGutter, highlightSpecialChars, keymap, lineNumbers } from '@codemirror/view'
import { EditorState, Compartment, StateEffect, Prec, Extension, Facet } from '@codemirror/state'
import { EventEmitter } from "./event-emitter";
import { deleteTrailingWhitespace, defaultKeymap, historyKeymap, indentWithTab } from '@codemirror/commands'
import { history } from "@codemirror/commands"
import { indentOnInput, defaultHighlightStyle, syntaxHighlighting, LanguageSupport, indentUnit, indentService } from "@codemirror/language"
import { highlightSelectionMatches, searchKeymap } from "@codemirror/search";
import {
    errorLineField, debugLineField, decorationsTheme, addDebugLine,
    addErrorLine, addErrorWord, removeDebugLine, removeErrorMarkers,
    breakpointGutterState, breakpointGutter, addIncorrectLineEffect,
    incorrectLineField,
    removeIncorrectLineEffect,
    addDebugWords,
    placeholders,
    basicIndent,
    variableHighlighter
} from "./cm-decorations";
import { LRLanguage } from "@codemirror/language"
import { languagePerLevel } from "./lezer-parsers/language-packages";
import { theGlobalSourcemap, theLevel } from "./app";
import { monokai } from "./cm-monokai-theme";
import { error } from "./modal";
import { ClientMessages } from "./client-messages";
import { Tag, styleTags, tags as t } from "@lezer/highlight";


// CodeMirror requires # of indentation to be in spaces.
const indentSize = ' '.repeat(4);
export const level = Facet.define<number, number>();

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
    private editorEvent = new EventEmitter<EditorEvent>({
        change: true,
        guttermousedown: true,
        changeBreakpoint: true,
        click: true
    });
    private currentDebugLine?: number;
    private incorrectLineMapping: Record<string, number> = {};

    constructor(element: HTMLElement, isReadOnly: boolean, editorType: EditorType, __: string = "ltr") {
        let state: EditorState;
        if (editorType === EditorType.MAIN) {

            const mainEditorStyling = EditorView.theme({
                "&": {
                    background: '#272822',
                    fontSize: '15.2px',
                    color: 'white',
                    borderRadius: '4px',
                    marginRight: '5px'
                },

                ".cm-scroller": {
                    overflow: "auto"
                },

                ".cm-gutters": {
                    borderRadius: '4px'
                },            
                ".cm-cursor, .cm-dropCursor": {borderLeftColor: "white", borderLeftWidth: "2px"},
                
                ".cm-name": {
                    color: '#009975'
                },
            });

            state = EditorState.create({
                doc: '',
                extensions: [
                    mainEditorStyling,
                    breakpointGutter,
                    lineNumbers(),
                    highlightActiveLineGutter(),
                    highlightSpecialChars(),
                    history(),
                    drawSelection(),
                    dropCursor(),
                    // When we finish doing the language package for Hedy, we need to add a configuration for this field to work
                    indentOnInput(),
                    syntaxHighlighting(defaultHighlightStyle, { fallback: true }),
                    highlightActiveLine(),
                    highlightSelectionMatches(),
                    keymap.of([
                        ...defaultKeymap,
                        ...searchKeymap, // we need to replace this with our own search widget
                        ...historyKeymap,
                        indentWithTab,
                    ]),
                    indentUnit.of(indentSize),
                    indentService.of(basicIndent),
                    monokai,
                    this.readMode.of(EditorState.readOnly.of(isReadOnly)),
                    errorLineField,
                    debugLineField,
                    incorrectLineField,
                    Prec.high(decorationsTheme),
                    placeholders,
                    theLevel ? level.of(theLevel) : [],
                    Prec.highest(variableHighlighter)
                ]
            });
        } else { // the editor is a read only editor
            let theme: Record<string, any> = {
                ".cm-cursor, .cm-dropCursor": { border: "none"},
                
                ".cm-name": {
                    color: '#009975'
                },
            }
            // base set of extensions for every type of read-only editor
            let extensions: Extension[] = [
                highlightSpecialChars(),
                drawSelection(),
                syntaxHighlighting(defaultHighlightStyle, { fallback: true }),
                monokai,
                this.readMode.of(EditorState.readOnly.of(isReadOnly)),
                placeholders,
                theLevel ? level.of(theLevel) : [],
                Prec.high(decorationsTheme),
                Prec.highest(variableHighlighter)
            ];

            switch(editorType) {
                case EditorType.CHEATSHEET:
                case EditorType.EXAMPLE:
                case EditorType.PARSONS:
                    theme[".cm-scroller"] = { "overflow": "auto", "min-height": "3.5rem" }
                    extensions.push(EditorView.theme(theme));
                    break;
                case EditorType.COMMON_MISTAKES: 
                    theme["&"] = {
                        background: '#272822',
                        fontSize: '15.2px',
                        color: 'white',
                        borderRadius: '4px',
                        marginRight: '5px'
                    }                
                    extensions.push([
                        EditorView.theme(theme),
                        lineNumbers(),
                        highlightActiveLine(),
                        highlightActiveLineGutter()
                    ]);
                    break;
            }
            
            state = EditorState.create({
                doc: '',
                extensions: extensions
            });
        }

        this.view = new EditorView({
            parent: element,
            state: state
        });

        if (theLevel) {
            this.setHighlighterForLevel(theLevel);
        }
    }

    /**
    * Set the highlither rules for a particular level
    * @param level
    */
    setHighlighterForLevel(level: number): void {
        const language = languagePerLevel[level];
        // Contains all of the keywords for every level
        const hedyStyleTags: Record<string, Tag> = {
            "print forward turn play color ask is echo sleep Comma": t.keyword,
            "at random remove from add to if else in not_in Op": t.keyword,
            "repeat times for range with return and or while": t.keyword,
            "elif def input toList": t.keyword,
            "true false True False": t.number,
            Comment: t.lineComment,
            "Text": t.name,
            "String": t.string,
            "clear pressed": t.color,
            "Number Int": t.number,
            "define call": t.operatorKeyword,
            "Command/ErrorInvalid/Text": t.invalid,
        }

        const parserWithMetadata = language.configure({
            props: [
                styleTags(hedyStyleTags)
            ]
        })

        const langPackage = LRLanguage.define({
            parser: parserWithMetadata,
            languageData: {
                commentTokens: { line: "#" }
            }
        })

        function hedy() {
            return new LanguageSupport(langPackage)
        }

        const effect = StateEffect.appendConfig.of(hedy());

        this.view.dispatch({ effects: effect });
        const transaction = this.view.state.update({
            effects: StateEffect.appendConfig.of(EditorView.updateListener.of((v: ViewUpdate) => {
                if (v.docChanged) {
                    console.log(language.parse(v.state.doc.toString()).toString());
                }
            }))
        })
        this.view.dispatch(transaction);
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
     * Resizes the editor after changing its size programatically (provide size in rem)
     */
    resize(newHeightRem?: number): void {
        if (newHeightRem === undefined) {
            console.log('Error! When resizing a CodeMirror instance, you need to provide the new height');
            return;
        }
        console.warn('Oops! editor.resize() should not have been called anymore');
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
        let effect: StateEffect<void> = removeErrorMarkers.of();
        this.view.dispatch({ effects: effect });
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
        } else if (key === 'click') {
            const eventHandler = EditorView.domEventHandlers({
                click: handler
            });
            const effect = StateEffect.appendConfig.of(eventHandler);
            this.view.dispatch({ effects: effect });
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
     * 'length' characters, unless the length of the string to highlight is 0.
     *
     * If that's the case, highlight the whole line
     *
     * 'row' and 'col' are 1-based.
     */
    highlightError(row: number, col?: number) {
        let effect: StateEffect<{ row: number, col?: number }>;
        if (col === undefined) {
            effect = addErrorLine.of({ row });
        } else {
            effect = addErrorWord.of({ row, col });
        }
        this.view.dispatch({ effects: effect })
    }

    /**
     * Remove all incorrect lines markers
     */
    // clearIncorrectLines(): void => for Skip Faulty

    /**
     * Set the current line in the debugger
     */
    setDebuggerCurrentLine(line?: number, startPos?: number, finishPos?: number) {
        if (this.currentDebugLine) {
            this.view.dispatch({ effects: removeDebugLine.of() });
        }

        if (line === undefined) {
            this.currentDebugLine = undefined;
            return;
        }

        this.currentDebugLine = line;
        if (startPos !== undefined && finishPos !== undefined) {
            let effect: StateEffect<{ from: number, to: number }>
            const docLine = this.view.state.doc.line(line);
            const from = docLine.from + startPos - 1;
            const to = docLine.from + finishPos;
            effect = addDebugWords.of({ from, to });
            this.view.dispatch({ effects: effect });
        } else {
            let effect: StateEffect<{ row: number }>;
            effect = addDebugLine.of({ row: line });
            this.view.dispatch({ effects: effect });
        }
    }

    getActiveContents(debugLine: string | null): string {
        // Do nothing if the code is empty
        const currentContent = this.view.state.doc.toString();
        if (currentContent === '') {
            return '';
        }
        const gutterMarkers = this.view.state.field(breakpointGutterState);
        const deactivatedLines: number[] = []
        let to: number;
        let lines: string[];
        if (debugLine === null) {
            to = this.view.state.doc.length;
            lines = currentContent.split('\n');
        } else {
            // After getting rid of Ace, we can start indexing debugLine 1-based
            const currentDebugLine = parseInt(debugLine, 10) + 1;
            to = this.view.state.doc.line(currentDebugLine).to;
            lines = currentContent.split('\n').slice(0, currentDebugLine);
        }
        gutterMarkers.between(0, to, (from: number) => {
            deactivatedLines.push(this.view.state.doc.lineAt(from).number);
        });
        const resultingLines = [];
        for (let i = 0; i < lines.length; i++) {
            if (deactivatedLines.includes(i + 1)) {
                resultingLines.push('');
            } else {
                resultingLines.push(lines[i]);
            }
        }
        const code = resultingLines.join('\n');
        return code;
    }

    setIncorrectLine(range: SourceRange, lineIndex: number): void {
        const startLine = this.view.state.doc.line(range.startLine);
        const endLine = this.view.state.doc.line(range.endLine);
        const from = startLine.from + range.startColumn - 1;
        let to = endLine.from + range.endColumn - 1;
        // Sometimes to exceeds the length of the line
        to = to > endLine.to ? endLine.to : to;
        this.incorrectLineMapping[`${from}-${to}`] = lineIndex;
        let effect = addIncorrectLineEffect.of({ from, to });
        this.view.dispatch({ effects: effect });
    }

    clearIncorrectLines(): void {
        this.incorrectLineMapping = {};
        const effect = removeIncorrectLineEffect.of();
        this.view.dispatch({ effects: effect });
    }

    getPosFromCoord(x: number, y: number): number | null {
        return this.view.posAtCoords({ x, y });
    }

    /**
     * Returns index of the error in the source map for this position
     * null if there's no error here
     * @param pos
     */
    indexOfErrorInPos(pos: number): number | null {
        const incorrectLineSet = this.view.state.field(incorrectLineField);
        let index = null;
        incorrectLineSet.between(pos, pos, (from: number, to: number) => { index = this.incorrectLineMapping[`${from}-${to}`] });
        return index;
    }

    hasIncorrectLinesDecorations(): boolean {
        const incorrectLineSet = this.view.state.field(incorrectLineField);
        let hasIncorrectLines = false;
        incorrectLineSet.between(0, this.view.state.doc.length, () => { hasIncorrectLines = true });
        return hasIncorrectLines
    }

    public skipFaultyHandler(event: MouseEvent): void {
        if (!this.hasIncorrectLinesDecorations()) return;
        const pos = this.getPosFromCoord(event.x, event.y);
        if (pos == null) return;
        const index = this.indexOfErrorInPos(pos)
        if (index == null) {
            // Hide error, warning or okbox
            error.hide();
        } else {
            // Show error for this line
            let mapError = theGlobalSourcemap[index];
            error.hide();
            error.show(ClientMessages['Transpile_error'], mapError.error);
        }
    }
}
