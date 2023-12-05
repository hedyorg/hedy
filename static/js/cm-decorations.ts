import { Decoration, DecorationSet, EditorView, GutterMarker, MatchDecorator, ViewPlugin, ViewUpdate, gutter, } from '@codemirror/view'
import { RangeSet, RangeSetBuilder, StateEffect, StateField } from '@codemirror/state'
import {syntaxTree} from "@codemirror/language"
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
        color: '#EDF492 ',
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
import { WidgetType } from "@codemirror/view"

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

function highlightVariables(view: EditorView) {
    let variableDeco = new RangeSetBuilder<Decoration>()
    for (let {from, to} of view.visibleRanges) {
        syntaxTree(view.state).iterate({
            from: from,
            to: to,
            enter: (node) => {
                if (node.name === 'Assign') {                                       
                    const child = node.node.getChild('Text');
                    if (child) {                        
                        console.log(view.state.doc.sliceString(child.from, child.to))
                        variableDeco.add(child.from, child.to, highlightVariableMarker)
                    }
                }
            }
        })
    }

    return variableDeco.finish()
}