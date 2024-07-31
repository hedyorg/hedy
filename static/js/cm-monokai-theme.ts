import {EditorView} from "@codemirror/view"
import {Extension} from "@codemirror/state"
import {HighlightStyle, syntaxHighlighting} from "@codemirror/language"
import {tags as t} from "@lezer/highlight"

const strawberry = "#ff6188",
    greenLizard = "#a6e22e",
    whiskey = "#d19a66",
    ivory = "#abb2bf",
    darkSilver = "#75715e",
    coral = "#e06c75",
    invalid = "#ffffff",
    stone = "#7d8799", 
    malibu = "#61afef",
    violet = "#ae81ff",
    background = "#272822",
    highlightBackground = "#202020",
    selection = "#90cdf463",
    gutterBackground = "#2F3129",
    gutterColor = "#8F908A",
    activeLineGutter = "#272727",
    skyBlue = "#66D9EF",
    // we don't really use these two, might need to edit them in the future
    tooltipBackground = "#353a42",
    darkBackground = "#21252b"

  /// The colors used in the theme, as CSS color strings.
export const color = {
  coral,
  invalid,
  ivory,
  stone,
  malibu,
  violet,
  whiskey,
  greenLizard,
  strawberry,
  darkSilver,
  background,
  selection,
  gutterBackground,
  gutterColor,
  activeLineGutter
}

/// The editor theme styles for One Dark.
export const monokaiTheme = EditorView.theme({
  "&": {
    color: ivory,
    backgroundColor: background
  },

  ".cm-content": {
    caretColor: "white"
  },

  ".cm-cursor, .cm-dropCursor": {borderLeftColor: "white"},
  "&.cm-focused > .cm-scroller > .cm-selectionLayer .cm-selectionBackground, .cm-selectionBackground, .cm-content ::selection": {backgroundColor: selection, borderRadius: "2px"},

  ".cm-panels": {backgroundColor: darkBackground, color: ivory},
  ".cm-panels.cm-panels-top": {borderBottom: "2px solid black"},
  ".cm-panels.cm-panels-bottom": {borderTop: "2px solid black"},

  ".cm-searchMatch": {
    backgroundColor: "#72a1ff59",
    outline: "1px solid #457dff"
  },
  ".cm-searchMatch.cm-searchMatch-selected": {
    backgroundColor: "#6199ff2f"
  },

  ".cm-activeLine": {backgroundColor: "#706d6d15"},
  ".cm-selectionMatch": {backgroundColor: "#aafe661a"},

  "&.cm-focused .cm-matchingBracket, &.cm-focused .cm-nonmatchingBracket": {
    backgroundColor: "#bad0f847"
  },

  ".cm-gutters": {
    backgroundColor: gutterBackground,
    color: gutterColor,
    border: "none"
  },

  ".cm-activeLineGutter": {
    backgroundColor: "#85828215",
    color: "white"
  },

  ".cm-foldPlaceholder": {
    backgroundColor: "transparent",
    border: "none",
    color: "#ddd"
  },

  ".cm-tooltip": {
    border: "none",
    backgroundColor: tooltipBackground
  },
  ".cm-tooltip .cm-tooltip-arrow:before": {
    borderTopColor: "transparent",
    borderBottomColor: "transparent"
  },
  ".cm-tooltip .cm-tooltip-arrow:after": {
    borderTopColor: tooltipBackground,
    borderBottomColor: tooltipBackground
  },
  ".cm-tooltip-autocomplete": {
    "& > ul > li[aria-selected]": {
      backgroundColor: highlightBackground,
      color: ivory
    }
  }
}, {dark: true})


/// The highlighting style for code in the monokai theme
export const monokaiHighlightStyle = HighlightStyle.define([
  {tag: t.keyword,
   color: strawberry},
  {tag: [t.name, t.deleted, t.character, t.propertyName, t.macroName],
   color: "white"},
  {tag: [t.function(t.variableName), t.labelName],
   color: malibu},
  {tag: [t.color, t.constant(t.name), t.standard(t.name)],
   color: whiskey},
  {tag: [t.definition(t.name), t.separator],
   color: ivory},
  {tag: [t.typeName, t.className, t.number, t.changed, t.annotation, t.modifier, t.self, t.namespace],
   color: greenLizard},
  {tag: [t.operator, t.operatorKeyword, t.url, t.escape, t.regexp, t.link, t.special(t.string)],
   color: skyBlue},
  {tag: [t.meta, t.comment],
   color: darkSilver},
  {tag: t.strong,
   fontWeight: "bold"},
  {tag: t.emphasis,
   fontStyle: "italic"},
  {tag: t.strikethrough,
   textDecoration: "line-through"},
  {tag: t.link,
   color: stone,
   textDecoration: "underline"},
  {tag: t.heading,
   fontWeight: "bold",
   color: coral},
  {tag: [t.atom, t.bool, t.special(t.variableName)],
   color: whiskey },
  {tag: [t.processingInstruction, t.string, t.inserted],
   color: violet},
  {tag: t.invalid,
   color: ivory},
])

/// Extension to enable the Monokai theme (both the editor theme and
/// the highlight style).
export const monokai: Extension = [monokaiTheme, syntaxHighlighting(monokaiHighlightStyle)]
