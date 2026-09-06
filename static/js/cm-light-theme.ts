import { EditorView } from "@codemirror/view"
import { Extension } from "@codemirror/state"
import { HighlightStyle, syntaxHighlighting } from "@codemirror/language"
import { tags as t } from "@lezer/highlight"

/**
 * A light counterpart to the monokai theme, for read-only code shown inside a page
 * that reads as a document rather than as an editor.
 *
 * The colours are Hedy's own: the ground and the keyword colour are the same pair the
 * page uses for inline keywords in prose, so a keyword reads the same whether it sits
 * in a sentence or in an example. Every tag monokai styles is styled here too, because
 * anything left out falls through to CodeMirror's default highlight style, which is
 * tuned for a different palette.
 */
const ink = "#2d3748",           // gray-800, ordinary code
    keyword = "#e53e3e",         // red-600, matches inline keywords in prose
    string = "#6b46c1",          // purple-700
    number = "#2f855a",          // green-700
    operator = "#2b6cb0",        // blue-700
    functionName = "#2c5282",    // blue-800
    constant = "#b7791f",        // yellow-700
    comment = "#718096",         // gray-600
    invalid = "#9b2c2c",         // red-800
    link = "#2b6cb0",
    background = "#edf2f7",      // gray-200
    // On a light ground the active line reads better lighter than its surroundings
    // than darker: it lifts the current line instead of shading it.
    highlightBackground = "#f7fafc",
    selection = "#bee3f8",       // blue-200
    gutterBackground = "#e2e8f0",
    gutterColor = "#a0aec0",
    activeLineGutter = "#f7fafc"

/// The colors used in the theme, as CSS color strings.
export const lightColor = {
    ink,
    keyword,
    string,
    number,
    operator,
    functionName,
    constant,
    comment,
    background,
    selection,
    gutterBackground,
    gutterColor,
    activeLineGutter
}

/// The editor theme styles for the light theme.
export const lightTheme = EditorView.theme({
    "&": {
        color: ink,
        backgroundColor: background
    },

    ".cm-content": {
        caretColor: ink
    },

    ".cm-cursor, .cm-dropCursor": { borderLeftColor: ink },
    "&.cm-focused > .cm-scroller > .cm-selectionLayer .cm-selectionBackground, .cm-selectionBackground, .cm-content ::selection": { backgroundColor: selection, borderRadius: "2px" },

    ".cm-activeLine": { backgroundColor: highlightBackground },

    ".cm-gutters": {
        backgroundColor: gutterBackground,
        color: gutterColor,
        border: "none"
    },

    ".cm-activeLineGutter": {
        backgroundColor: activeLineGutter,
        color: ink
    },

    /*
      These three carry colours picked for a dark ground and are invisible on a light
      one, so the light theme has to restate them. `.cm-name` is set by the read-only
      editor itself; the two highlights come from `decorationsTheme`.
    */
    ".cm-name": { color: "#2c7a7b" },
    ".cm-highlight-var": { color: "#2b6cb0" },
    ".cm-highlight-fun": { color: "#975a16" }
}, { dark: false })

/// The highlighting style for code in the light theme.
export const lightHighlightStyle = HighlightStyle.define([
    { tag: t.keyword, color: keyword },
    {
        tag: [t.name, t.deleted, t.character, t.propertyName, t.macroName],
        color: ink
    },
    {
        tag: [t.function(t.variableName), t.labelName],
        color: functionName
    },
    {
        tag: [t.color, t.constant(t.name), t.standard(t.name)],
        color: constant
    },
    {
        tag: [t.definition(t.name), t.separator],
        color: ink
    },
    {
        tag: [t.typeName, t.className, t.number, t.changed, t.annotation, t.modifier, t.self, t.namespace],
        color: number
    },
    {
        tag: [t.operator, t.operatorKeyword, t.url, t.escape, t.regexp, t.link, t.special(t.string)],
        color: operator
    },
    {
        tag: [t.meta, t.comment],
        color: comment,
        fontStyle: "italic"
    },
    { tag: t.strong, fontWeight: "bold" },
    { tag: t.emphasis, fontStyle: "italic" },
    { tag: t.strikethrough, textDecoration: "line-through" },
    {
        tag: t.link,
        color: link,
        textDecoration: "underline"
    },
    {
        tag: t.heading,
        fontWeight: "bold",
        color: keyword
    },
    {
        tag: [t.atom, t.bool, t.special(t.variableName)],
        color: constant
    },
    {
        tag: [t.processingInstruction, t.string, t.inserted],
        color: string
    },
    { tag: t.invalid, color: invalid },
])

/// Extension to enable the light theme (both the editor theme and
/// the highlight style).
export const light: Extension = [lightTheme, syntaxHighlighting(lightHighlightStyle)]
