import { HedyEditor, EditorType, HedyEditorCreator, EditorEvent, SourceRange } from "./editor";
import { EditorView, ViewUpdate, drawSelection, dropCursor, highlightActiveLine, 
        highlightActiveLineGutter, highlightSpecialChars, keymap, lineNumbers } from '@codemirror/view'
import { EditorState, Compartment, StateEffect, Prec } from '@codemirror/state'
import { oneDark } from '@codemirror/theme-one-dark';
import { EventEmitter } from "./event-emitter";
import { deleteTrailingWhitespace, defaultKeymap, historyKeymap } from '@codemirror/commands'
import { history } from "@codemirror/commands"
import { indentOnInput, defaultHighlightStyle, syntaxHighlighting ,LanguageSupport } from "@codemirror/language"
import { highlightSelectionMatches, searchKeymap } from "@codemirror/search";
import { 
    errorLineField, debugLineField, decorationsTheme, addDebugLine, 
    addErrorLine, addErrorWord, removeDebugLine, removeErrorMarkers, 
    breakpointGutterState, breakpointGutter, addIncorrectLineEffect,
    incorrectLineField,
    removeIncorrectLineEffect
} from "./cm-decorations";


import { parser as level1Parser } from "./lezer-parsers/level1-parser.js"
import { parser as level2Parser } from "./lezer-parsers/level2-parser.js"
import { parser as level3Parser } from "./lezer-parsers/level3-parser"
import { parser as level4Parser } from "./lezer-parsers/level4-parser"
import { parser as level5Parser } from "./lezer-parsers/level5-parser"
import { parser as level6Parser } from "./lezer-parsers/level6-parser"
import { parser as level7Parser } from "./lezer-parsers/level7-parser"
import { parser as level8Parser } from "./lezer-parsers/level8-parser"
import { parser as level10Parser } from "./lezer-parsers/level10-parser"
import { parser as level11Parser } from "./lezer-parsers/level11-parser"
import { parser as level12Parser } from "./lezer-parsers/level12-parser"
import { parser as level13Parser } from "./lezer-parsers/level13-parser"
import { parser as level14Parser } from "./lezer-parsers/level14-parser"
import { parser as level15Parser } from "./lezer-parsers/level15-parser"

import { styleTags, tags as t } from "@lezer/highlight";
import {LRLanguage} from "@codemirror/language"

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
        changeBreakpoint: true,
        click: true
    });
    private currentDebugLine?: number;
    private incorrectLineMapping: Record<string, number> = {};

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
            }
        }

        const cursorStyle = { ".cm-cursor, .cm-dropCursor": {borderLeftColor: "white", borderLeftWidth: "2px"} }

        const mainEditorStyling = EditorView.theme(this.themeStyles);

        let parserWithMetadata15 = level15Parser.configure({
            props: [
                styleTags({
                        "print forward turn color ask is echo sleep Comma at random remove from add to if else in not Op repeat times for range with return and or while": t.keyword,
                        "Assign/IsToken": t.keyword,      
                        Comment: t.lineComment,                        
                        "String quote": t.string,
                        "clear pressed": t.color,
                        "Int Number": t.number,
                        "define call": t.operatorKeyword,
                        "Command/ErrorInvalid/Text Command/ErrorInvalid/TextWithoutSpaces": t.invalid,
                    })
                ]
            })
            
            const level15Language = LRLanguage.define({
                    parser: parserWithMetadata15,
                    languageData: {
                            commentTokens: {line: "#"}
                        }
        })
        
        function hedyLevel15() {
            return new LanguageSupport(level15Language)
        }

        
        let parserWithMetadata14 = level14Parser.configure({
            props: [
                styleTags({
                        "print forward turn color ask is echo sleep Comma at random remove from add to if else in not Op repeat times for range with return and or": t.keyword,
                        "Assign/IsToken": t.keyword,      
                        Comment: t.lineComment,                        
                        "String quote": t.string,
                        "clear pressed": t.color,
                        "Int Number": t.number,
                        "define call": t.operatorKeyword,
                        "Command/ErrorInvalid/Text Command/ErrorInvalid/TextWithoutSpaces": t.invalid,
                    })
                ]
            })
            
            const level14Language = LRLanguage.define({
                    parser: parserWithMetadata14,
                    languageData: {
                            commentTokens: {line: "#"}
                        }
        })
        
        function hedyLevel14() {
            return new LanguageSupport(level14Language)
        }

        let parserWithMetadata13 = level13Parser.configure({
            props: [
                styleTags({
                        "print forward turn color ask is echo sleep Comma at random remove from add to if else in not Op repeat times for range with return and or": t.keyword,
                        "Assign/IsToken": t.keyword,      
                        Comment: t.lineComment,                        
                        "String quote": t.string,
                        "clear pressed": t.color,
                        "Int Number": t.number,
                        "define call": t.operatorKeyword,
                        "Command/ErrorInvalid/Text Command/ErrorInvalid/TextWithoutSpaces": t.invalid,
                    })
                ]
            })
            
            const level13Language = LRLanguage.define({
                    parser: parserWithMetadata13,
                    languageData: {
                            commentTokens: {line: "#"}
                        }
        })
        
        function hedyLevel13() {
            return new LanguageSupport(level13Language)
        }


        let parserWithMetadata12 = level12Parser.configure({
            props: [
                styleTags({
                        "print forward turn color ask is echo sleep Comma at random remove from add to if else in not Op repeat times for range with return": t.keyword,
                        "Assign/IsToken": t.keyword,      
                        Comment: t.lineComment,                        
                        "String quote": t.string,
                        "clear pressed": t.color,
                        "Int Number": t.number,
                        "define call": t.operatorKeyword,
                        "Command/ErrorInvalid/Text Command/ErrorInvalid/TextWithoutSpaces": t.invalid,
                    })
                ]
            })
            
            const level12Language = LRLanguage.define({
                    parser: parserWithMetadata12,
                    languageData: {
                            commentTokens: {line: "#"}
                        }
        })
        
        function hedyLevel12() {
            return new LanguageSupport(level12Language)
        }

        let parserWithMetadata11 = level11Parser.configure({
            props: [
                styleTags({
                        "print forward turn color ask is echo sleep Comma at random remove from add to if else in not Op repeat times for range": t.keyword,
                        "Assign/IsToken": t.keyword,      
                        Comment: t.lineComment,                        
                        "String quote": t.string,
                        "clear pressed": t.color,
                        "Int": t.number,
                        "Command/ErrorInvalid/Text Command/ErrorInvalid/TextWithoutSpaces": t.invalid,
                    })
                ]
            })
            
            const level11Language = LRLanguage.define({
                    parser: parserWithMetadata11,
                    languageData: {
                            commentTokens: {line: "#"}
                        }
        })
        
        function hedyLevel11() {
            return new LanguageSupport(level11Language)
        }
        let parserWithMetadata10 = level10Parser.configure({
            props: [
                styleTags({
                        "print forward turn color ask is echo sleep Comma at random remove from add to if else in not Op repeat times for": t.keyword,
                        "Assign/IsToken": t.keyword,      
                        Comment: t.lineComment,                        
                        "String quote": t.string,
                        "clear pressed": t.color,
                        "Int": t.number,
                        "Command/ErrorInvalid/Text Command/ErrorInvalid/TextWithoutSpaces": t.invalid,
                    })
                ]
            })
            
            const level10Language = LRLanguage.define({
                    parser: parserWithMetadata10,
                    languageData: {
                            commentTokens: {line: "#"}
                        }
        })
        
        function hedyLevel10() {
            return new LanguageSupport(level10Language)
        }
        
        let parserWithMetadata8 = level8Parser.configure({
            props: [
                styleTags({
                        "print forward turn color ask is echo sleep Comma at random remove from add to if else in not Op repeat times": t.keyword,
                        "Assign/IsToken": t.keyword,      
                        Comment: t.lineComment,                        
                        "String quote": t.string,
                        "clear pressed": t.color,
                        "Int": t.number,
                        "Command/ErrorInvalid/Text Command/ErrorInvalid/TextWithoutSpaces": t.invalid,
                    })
                ]
            })
            
            const level8Language = LRLanguage.define({
                    parser: parserWithMetadata8,
                    languageData: {
                            commentTokens: {line: "#"}
                        }
        })
        
        function hedyLevel8() {
            return new LanguageSupport(level8Language)
        }

        let parserWithMetadata7 = level7Parser.configure({
            props: [
                styleTags({
                        "print forward turn color ask is echo sleep Comma at random remove from add to if else in not Op repeat times": t.keyword,
                        "Assign/IsToken": t.keyword,      
                        Comment: t.lineComment,                        
                        "String quote": t.string,
                        "clear pressed": t.color,
                        "Int": t.number,
                        "Command/ErrorInvalid/Text Command/ErrorInvalid/TextWithoutSpaces": t.invalid,
                    })
                ]
            })
            
            const level7Language = LRLanguage.define({
                    parser: parserWithMetadata7,
                    languageData: {
                            commentTokens: {line: "#"}
                        }
        })
        
        function hedyLevel7() {
            return new LanguageSupport(level7Language)
        }


        let parserWithMetadata6 = level6Parser.configure({
            props: [
                styleTags({
                        "print forward turn color ask is echo sleep Comma at random remove from add to if else in not Op": t.keyword,
                        "Assign/IsToken": t.keyword,      
                        Comment: t.lineComment,                        
                        "String quote": t.string,
                        "clear pressed": t.color,
                        "Int": t.number,
                        "Command/ErrorInvalid/Text Command/ErrorInvalid/TextWithoutSpaces": t.invalid,
                    })
                ]
            })
            
            const level6Language = LRLanguage.define({
                    parser: parserWithMetadata6,
                    languageData: {
                            commentTokens: {line: "#"}
                        }
        })
        
        function hedyLevel6() {
            return new LanguageSupport(level6Language)
        }
        
        let parserWithMetadata5 = level5Parser.configure({
            props: [
                styleTags({
                        "print forward turn color ask is echo sleep Comma at random remove from add to if else in not": t.keyword,
                        "Assign/IsToken": t.keyword,      
                        Comment: t.lineComment,                        
                        "String quote": t.string,
                        "clear pressed": t.color,
                        "Command/ErrorInvalid/Text Command/ErrorInvalid/TextWithoutSpaces": t.invalid,
                    })
                ]
            })
            
            const level5Language = LRLanguage.define({
                    parser: parserWithMetadata5,
                    languageData: {
                            commentTokens: {line: "#"}
                        }
        })
        
        function hedyLevel5() {
            return new LanguageSupport(level5Language)
        }
        
        let parserWithMetadata4 = level4Parser.configure({
            props: [
                styleTags({
                        "print forward turn color ask is echo sleep Comma at random remove from add to": t.keyword,
                        "Assign/IsToken": t.keyword,      
                        Comment: t.lineComment,                        
                        "String quote": t.string,
                        "clear": t.color,
                        "Command/ErrorInvalid/Text Command/ErrorInvalid/TextWithoutSpaces": t.invalid,
                    })
                ]
            })
            
            const level4Language = LRLanguage.define({
                    parser: parserWithMetadata4,
                    languageData: {
                            commentTokens: {line: "#"}
                        }
        })
        
        function hedyLevel4() {
            return new LanguageSupport(level4Language)
        }

        let parserWithMetadata3 = level3Parser.configure({
            props: [
                styleTags({
                        "print forward turn color ask is echo sleep Comma at random remove from add to": t.keyword,
                        "Assign/IsToken": t.keyword,      
                        Comment: t.lineComment,                        
                        "Name": t.name,
                        "Command/ErrorInvalid/Text Command/ErrorInvalid/TextWithoutSpaces": t.invalid,
                    })
                ]
            })
            
            const level3Language = LRLanguage.define({
                    parser: parserWithMetadata3,
                    languageData: {
                            commentTokens: {line: "#"}
                        }
        })
        
        function hedyLevel3() {
            return new LanguageSupport(level3Language)
        }

        let parserWithMetadata2 = level2Parser.configure({
            props: [
                styleTags({
                        "print forward turn color ask is echo sleep": t.keyword,
                        "Assign/IsToken": t.keyword,
                        "Text AssignArgument/Name TextNo ": t.string,        
                        Comment: t.lineComment,                        
                        "Name": t.name,
                        "Command/ErrorInvalid/Text Command/ErrorInvalid/TextWithoutSpaces": t.invalid,
                    })
                ]
            })
            
            const level2Language = LRLanguage.define({
                    parser: parserWithMetadata2,
                    languageData: {
                            commentTokens: {line: "#"}
                        }
        })
        
        function hedyLevel2() {
            return new LanguageSupport(level2Language)
        }

        let parserWithMetadata = level1Parser.configure({
            props: [
                styleTags({
                    "print ask echo forward turn color": t.keyword,
                    Text: t.string,        
                    Comment: t.lineComment,
                    "Command/ErrorInvalid/Text Command/ErrorInvalid/TextWithoutSpaces": t.invalid,
                })
            ]
        })
            
        const level1Language = LRLanguage.define({
            parser: parserWithMetadata,
            languageData: {
                commentTokens: {line: "#"}
            }
        })

        function hedyLevel1() {
            return new LanguageSupport(level1Language)
        }

        const state = EditorState.create({
            doc: '',
            extensions: [                
                EditorView.theme(cursorStyle),
                breakpointGutter,
                lineNumbers(),
                highlightActiveLineGutter(),
                highlightSpecialChars(),
                history(),
                drawSelection(),
                dropCursor(),                
                // When we finish doing the language package for Hedy, we need to add a configuration for this field to work
                indentOnInput(),
                syntaxHighlighting(defaultHighlightStyle, {fallback: true}),                
                highlightActiveLine(),
                highlightSelectionMatches(),
                keymap.of([
                    ...defaultKeymap,
                    ...searchKeymap, // we need to replace this with our own search widget
                    ...historyKeymap,
                ]),
                oneDark,
                this.theme.of(mainEditorStyling),
                this.readMode.of(EditorState.readOnly.of(isReadOnly)),
                errorLineField,
                debugLineField,
                incorrectLineField,
                Prec.high(decorationsTheme),
                hedyLevel15()
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
        let effect: StateEffect<void> = removeErrorMarkers.of();
        this.view.dispatch({effects: effect});
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
                        console.log(level15Parser.parse(v.state.doc.toString()).toString());
                        handler();
                    }
                }))
            })
            this.view.dispatch(transaction);
        } else if (key === 'click') {
            const eventHandler = EditorView.domEventHandlers({
                click:  handler
            });
            const effect = StateEffect.appendConfig.of(eventHandler);
            this.view.dispatch({effects: effect});
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
        let effect: StateEffect<{row: number, col?: number}>;
        if (col === undefined) {
            effect = addErrorLine.of({row});
        } else {
            effect = addErrorWord.of({row, col});
        }
        this.view.dispatch({effects: effect})
    }

    /**
     * Remove all incorrect lines markers
     */
    // clearIncorrectLines(): void => for Skip Faulty

    /**
     * Set the current line in the debugger
     */
    setDebuggerCurrentLine(line: number | undefined) {        
        line = line === undefined ? line : line + 1;

        if (this.currentDebugLine === line) {
            return;
        }

        if (this.currentDebugLine) {
            this.view.dispatch({ effects: removeDebugLine.of() });
        }

        if (line === undefined) {
            this.currentDebugLine = undefined;
            return;
        }

        this.currentDebugLine = line;
        let effect: StateEffect<{row: number}>;
        effect = addDebugLine.of({row: line});
        this.view.dispatch({effects: effect});
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
        let effect = addIncorrectLineEffect.of({from, to});
        this.view.dispatch({effects: effect});
    }

    clearIncorrectLines(): void {
        this.incorrectLineMapping = {};
        const effect = removeIncorrectLineEffect.of();
        this.view.dispatch({effects: effect});
    }

    getPosFromCoord(x: number, y: number): number | null {
        return this.view.posAtCoords({x, y});
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
}