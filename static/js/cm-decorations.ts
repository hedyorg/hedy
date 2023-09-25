import { Decoration, DecorationSet, EditorView, } from '@codemirror/view'
import { StateEffect, StateField } from '@codemirror/state'


export const addErrorLine = StateEffect.define<{row: number}>();
export const addErrorWord = StateEffect.define<{row: number, col: number}>();
export const removeErrorMarkers = StateEffect.define<void>();

export const addDebugLine = StateEffect.define<{row: number}>();
export const removeDebugLine = StateEffect.define<void>();

export const errorLineField = StateField.define<DecorationSet>({
    create() {
      return Decoration.none;
    },
    update(errors, tr) {
      errors = errors.map(tr.changes);
      for (let e of tr.effects) {
        if (e.is(addErrorLine)) {
            // Get line given the row number
            const line = tr.state.doc.line(e.value.row);
            errors = errors.update({
                add: [errorHighlightLine.range(line.from, line.from)]
            });
        } else if(e.is(addErrorWord)) {
            const line = tr.state.doc.line(e.value.row);
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
        } else if (e.is(removeDebugLine)) {
            // Just return the empty decoration set to remove all of the errors
            return Decoration.none;
        }
      } 
      return errors;
    },
    provide: f => EditorView.decorations.from(f)
})
  
const errorHighlightLine = Decoration.line({class: "cm-error-editor"});
const errorHighlightMark = Decoration.mark({class: "cm-error-editor"});

const debugLine = Decoration.line({class: "cm-debugger-current-line"});

export const decorationsTheme = EditorView.theme({
    ".cm-error-editor": {
        outline: "2px solid #F56565",
        backgroundColor: "rgba(66, 153, 225, 0.7)",
        color: "white"
    },
    ".cm-debugger-current-line": {
        backgroundColor: "#2D6099"
    },
});