import { Decoration, DecorationSet, EditorView, GutterMarker, MatchDecorator, ViewPlugin, ViewUpdate, gutter, } from '@codemirror/view'
import { RangeSet, RangeSetBuilder, StateEffect, StateField } from '@codemirror/state'
import { IndentContext } from '@codemirror/language'
import {syntaxTree} from "@codemirror/language"
import { WidgetType } from "@codemirror/view"
import { SyntaxNode } from "@lezer/common"
import { level as levelFacet } from './cm-editor';

export const addErrorLine = StateEffect.define<{ row: number }>();
export const addErrorWord = StateEffect.define<{ row: number, col: number }>();
export const removeErrorMarkers = StateEffect.define<void>();

export const addDebugLine = StateEffect.define<{ row: number }>();
export const addDebugWords = StateEffect.define<{ from: number, to: number }>({
    map: (val, mapping) => ({ from: mapping.mapPos(val.from), to: mapping.mapPos(val.to) })
});
export const removeDebugLine = StateEffect.define<void>();

const breakpointGutterEffect = StateEffect.define<{ pos: number, on: boolean }>({
    map: (val, mapping) => ({ pos: mapping.mapPos(val.pos), on: val.on })
});

const deactivateLineEffect = StateEffect.define<{ pos: number, on: boolean }>({
    map: (val, mapping) => ({ pos: mapping.mapPos(val.pos), on: val.on })
});


export const addIncorrectLineEffect = StateEffect.define<{ from: number, to: number }>({
    map: (val, maping) => ({ from: maping.mapPos(val.from), to: maping.mapPos(val.to) })
});

export const removeIncorrectLineEffect = StateEffect.define<void>();

export const errorLineField = StateField.define<DecorationSet>({
    create() {
        return Decoration.none;
    },
    update(errors, transaction) {
        errors = errors.map(transaction.changes);
        for (let e of transaction.effects) {
            if (e.is(addErrorLine)) {
                // Get line given the row number
                const line = transaction.state.doc.line(e.value.row);
                errors = errors.update({
                    add: [errorHighlightLine.range(line.from, line.from)]
                });
            } else if (e.is(addErrorWord)) {
                const line = transaction.state.doc.line(e.value.row);
                const length = line.text.slice(e.value.col - 1).split(/(\s+)/)[0].length;
                if (length > 0) {
                    errors = errors.update({
                        add: [errorHighlightMark.range(line.from + e.value.col - 1, line.from + e.value.col - 1 + length)]
                    });
                } else { // If we can't find the word, highlight the whole line
                    errors = errors.update({
                        add: [errorHighlightLine.range(line.from, line.from)]
                    });
                }
            }
            else if (e.is(removeErrorMarkers)) {
                // Just return the empty decoration set to remove all of the errors
                return Decoration.none;
            }
        }
        return errors;
    },
    provide: f => EditorView.decorations.from(f)
});

export const debugLineField = StateField.define<DecorationSet>({
    create() {
        return Decoration.none;
    },
    update(errors, tr) {
        errors = errors.map(tr.changes);
        for (let e of tr.effects) {
            if (e.is(addDebugLine)) {
                // Get line given the row number
                const line = tr.state.doc.line(e.value.row);
                errors = errors.update({
                    add: [debugLine.range(line.from, line.from)]
                });
            } else if (e.is(addDebugWords)) {
                errors = errors.update({
                    add: [debugWord.range(e.value.from, e.value.to)]
                });
            } else if (e.is(removeDebugLine)) {
                // Just return the empty decoration set to remove all of the errors
                return Decoration.none;
            }
        }
        return errors;
    },
    provide: f => EditorView.decorations.from(f)
})

export const incorrectLineField = StateField.define<DecorationSet>({
    create() {
        return Decoration.none;
    },
    update(errors, tr) {
        errors = errors.map(tr.changes);
        for (let e of tr.effects) {
            if (e.is(addIncorrectLineEffect)) {
                errors = errors.update({
                    add: [incorrectCodeMark.range(e.value.from, e.value.to)]
                });
            } else if (e.is(removeIncorrectLineEffect)) {
                return Decoration.none;
            }
        }
        return errors;
    },
    provide: f => EditorView.decorations.from(f)
})

export const breakpointGutterState = StateField.define<RangeSet<GutterMarker>>({
    create() { return RangeSet.empty },
    update(set, transaction) {
        set = set.map(transaction.changes)
        for (let e of transaction.effects) {
            if (e.is(breakpointGutterEffect)) {
                if (e.value.on)
                    set = set.update({ add: [deactivateGutterMarker.range(e.value.pos)] })
                else
                    set = set.update({ filter: from => from != e.value.pos })
            }
        }
        return set
    }
});

const deactivateLineState = StateField.define<DecorationSet>({
    create() { return Decoration.none },
    update(set, transaction) {
        set = set.map(transaction.changes);
        for (let e of transaction.effects) {
            if (e.is(deactivateLineEffect)) {
                if (e.value.on) {
                    set = set.update({
                        add: [deactivateLineMarker.range(e.value.pos, e.value.pos)]
                    });
                } else {
                    set = set.update({
                        filter: from => from != e.value.pos
                    });
                }
            }
        }
        return set
    },
    provide: f => EditorView.decorations.from(f)
});

const errorHighlightLine = Decoration.line({ class: "cm-error-editor" });
const errorHighlightMark = Decoration.mark({ class: "cm-error-editor" });
const debugLine = Decoration.line({ class: "cm-debugger-current-line" });
const debugWord = Decoration.mark({ class: "cm-debugger-current-line" });
const incorrectCodeMark = Decoration.mark({ class: "cm-incorrect-hedy-code" });
const deactivateLineMarker = Decoration.line({ class: "cm-disabled-line" })
const highlightVariableMarker = Decoration.mark({ class: "cm-highlight-var"})
const highlightFunctionMarker = Decoration.mark({ class: "cm-highlight-fun"})

export const decorationsTheme = EditorView.theme({
    ".cm-error-editor": {
        outline: "2px solid #F56565",
        backgroundColor: "rgba(66, 153, 225, 0.7)",
        color: "white"
    },
    ".cm-debugger-current-line": {
        backgroundColor: "#2D6099"
    },
    ".cm-incorrect-hedy-code": {
        textDecoration: "red wavy underline",
    },
    ".cm-highlight-var": {
        color: '#c2e3ff ',
    },
    ".cm-highlight-fun": {
        color: "#EDF492",
    }
});


const deactivateGutterMarker = new class extends GutterMarker {
    toDOM() { return document.createTextNode("😴") }
}

function toggleLine(view: EditorView, pos: number) {
    let breakpoints = view.state.field(breakpointGutterState)
    let isDeactivated = false
    breakpoints.between(pos, pos, () => { isDeactivated = true })
    view.dispatch({
        effects: [
            breakpointGutterEffect.of({ pos, on: !isDeactivated }),
            deactivateLineEffect.of({ pos, on: !isDeactivated })
        ]
    })
}

export const breakpointGutter = [
    breakpointGutterState,
    deactivateLineState,
    gutter({
        class: "cm-breakpoint-gutter",
        markers: v => v.state.field(breakpointGutterState),
        initialSpacer: () => deactivateGutterMarker,
        domEventHandlers: {
            mousedown(view, line) {
                toggleLine(view, line.from)
                return true
            }
        }
    }),
    EditorView.baseTheme({
        ".cm-breakpoint-gutter .cm-gutterElement": {
            paddingLeft: "5px",
            cursor: "default"
        },
        ".cm-disabled-line": {
            textDecoration: "line-through"
        }
    })
]

class PlacheholderWidget extends WidgetType {
    constructor(readonly space: string, readonly placeholder: string) { super() }

    toDOM() {
        let wrap = document.createElement("span")
        wrap.setAttribute("aria-hidden", "true")
        wrap.style.setProperty('background', '#F92672')
        wrap.style.setProperty('color', 'white')
        wrap.innerHTML = '_'
        return wrap
    }

    ignoreEvent() { return false }
}

const placeholderMatcher = new MatchDecorator({
    regexp: /(?<![^ ])(_)(?= |$)/g,
    decoration: match => Decoration.replace({
        widget: new PlacheholderWidget(match[1], match[2]),
    })
})

export const placeholders = ViewPlugin.fromClass(class {
    placeholders: DecorationSet
    constructor(view: EditorView) {
      this.placeholders = placeholderMatcher.createDeco(view)
    }
    update(update: ViewUpdate) {
      this.placeholders = placeholderMatcher.updateDeco(update, this.placeholders)
    }
  }, {
    decorations: instance => instance.placeholders,
    provide: plugin => EditorView.atomicRanges.of(view => {
      return view.plugin(plugin)?.placeholders || Decoration.none
    })
})

export const variableHighlighter = ViewPlugin.fromClass(class {
    decorations: DecorationSet
    constructor(view: EditorView) {
      this.decorations = highlightVariables(view)
    }
    update(update: ViewUpdate) {
      if (update.docChanged || update.viewportChanged) {
        this.decorations = highlightVariables(update.view)
      }
    }
  }, {
    decorations: v => v.decorations
})
interface VariableData { 
    name: string, 
    type: "function" | "variable",
    pos: { from: number, to: number } 
}

function highlightVariables(view: EditorView) {
    const level = view.state.facet(levelFacet);
    // double equals because level is actually an array with just one element
    // like: [1]
    if (level == 1) return Decoration.none;
    let variableDeco = new RangeSetBuilder<Decoration>();
    let variableData: VariableData[] = []
    let functionsNames = new Set<string>()
    let variablesNames = new Set<string>()

    let definingCommands = [
        'Assign' , 
        'Ask' , 
        'AssignList' , 
        'For',
        "Input"
    ]
    // First we iterate through the tree to find all var assignments
    // To highlight them, but also to find the names of the variables
    // For later use in other rules
    for (let {from, to} of view.visibleRanges) {
        syntaxTree(view.state).iterate({
            from: from,
            to: to,
            enter: (node) => {
                if (definingCommands.includes(node.node.name)) {
                    const child = node.node.getChild('Text');
                    addVar(child, variableData, 'variable', view, functionsNames, variablesNames);                    
                } else if (node.node.name  === 'Define') {                    
                   const textChild = node.node.getChild('Text')
                    addVar(textChild, variableData, 'function', view, functionsNames, variablesNames)
                    // we need to get the parameter nodes that are within define nodes
                    const argumentChild = node.node.getChild('Arguments')
                    const expressions = argumentChild?.getChildren('Expression');
                    expressions?.map(expression => {
                        const textChild = expression.getChild('Text')
                        addVar(textChild, variableData, 'variable', view, functionsNames, variablesNames);
                    })
                }
            }
        })
    }

    let commands = [
        "Assign" , 
        "Print" , 
        "Forward", 
        "Turn", 
        "Color", 
        "Sleep", 
        "ListAccess", 
        "Add", 
        "Remove",
        "EqualityCheck",
        "InListCheck",
        "NotInListCheck",
        "Expression",
        "Repeat",
        "For",
        "Call",
        "Play"
    ]
    // in levels 2 and 3 variables are not substitued inside ask
    // not sure if that's intended behaviour or not
    if (level > 3) commands.push("Ask")
    // Now that we have the variable names, we can distinguish them from other Text nodes
    for (let {from, to} of view.visibleRanges) {
        syntaxTree(view.state).iterate({
            from: from,
            to: to,
            enter: (node) => {
                if (commands.includes(node.name)) {
                    const children = node.node.getChildren('Text');
                    // no need to add again the first child of defining commands since 
                    // we already highlighted it in the previous step
                    let i = definingCommands.includes(node.name) ? 1 : 0
                    for (; i < children.length; i++) {
                        const child = children[i];
                        const text = view.state.doc.sliceString(child.from, child.to);
                        // On level 2, since there aren't distinctions between strings and variable names
                        // It's possible to have several variables in the same text nodes
                        // separated by other characters like: name!!!your_name
                        // Therefore, we need to get the variables names inside this text node
                        if (level <= 3) {
                            const varNames = getVarNames(text) || [];
                            // we keep track of the index of the last variable viewed
                            let startIndex = 0;
                            for (const name of varNames) {
                                if (variablesNames.has(name)) {
                                    const index = text.indexOf(name, startIndex)
                                    variableData.push({
                                        name: name,
                                        type: 'variable', // there aren't functions until level 12
                                        pos: {from: child.from + index, to: child.from + index + name.length}
                                    })
                                    startIndex = index + name.length
                                }
                            }
                        } else if (variablesNames.has(text) || functionsNames.has(text)) {                  
                            variableData.push({
                                name: text,
                                type: variablesNames.has(text) ? 'variable' : 'function',
                                pos: {from: child.from, to: child.to}
                            })
                        }
                    }
                }
            }
        })
    }
    // I don't think we're going to have a huge document, so this won't overflow
    variableData.sort((a, b) => a.pos.from - b.pos.from)
    // If the decorations aren't sorted by starting position, CodeMirror complains, hence the need to do it like this
    variableData.forEach(data => {
        if (data.type === "function") {
            variableDeco.add(data.pos.from, data.pos.to, highlightFunctionMarker)
        } else {
            variableDeco.add(data.pos.from, data.pos.to, highlightVariableMarker)
        }
    })

    return variableDeco.finish()
}

function getVarNames(name: string) {
    const varRegex = /^[\p{Lu}\p{Ll}\p{Lt}\p{Lm}\p{Lo}\p{Nl}_]+([\p{Lu}\p{Ll}\p{Lt}\p{Lm}\p{Lo}\p{Nl}_]+|[\p{Mn}\p{Mc}\p{Nd}\p{Pc}·]+)*$/gmu
    return name.match(varRegex);
}

function isVarName(name: string) {
    const varRegex = /^[\p{Lu}\p{Ll}\p{Lt}\p{Lm}\p{Lo}\p{Nl}_]+([\p{Lu}\p{Ll}\p{Lt}\p{Lm}\p{Lo}\p{Nl}_]+|[\p{Mn}\p{Mc}\p{Nd}\p{Pc}·]+)*$/gmu
    return varRegex.test(name);
}

export function basicIndent(context: IndentContext, pos: number) {
    const nextIndentationSize = context.lineIndent(pos, -1);
    let prevIndentationSize;
    try {
        prevIndentationSize = context.lineIndent(pos + 1, -1);
    } catch (error) {
        prevIndentationSize = 0;
    }
    const indentBy = Math.max(
        prevIndentationSize,
        nextIndentationSize
    );
    return indentBy;

}

function addVar(child: SyntaxNode | null, variableData: VariableData[], type: "function" | "variable", view: EditorView, functionsNames: Set<string>, variablesNames: Set<string>) {
    if (child && isVarName(view.state.doc.sliceString(child.from, child.to))) {
        const name = view.state.doc.sliceString(child.from, child.to);
        const data: VariableData = {
            name: name,
            type: type,
            pos: {from: child.from, to: child.to}
        }
        variableData.push(data);
        switch(type) {
            case 'function':
                functionsNames.add(name);
                break;
            case 'variable':
                variablesNames.add(name);
                break;
        }
    } 
}