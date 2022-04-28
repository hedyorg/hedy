
## General Idea ##

Syntactic coloring uses 2 paradigms which are used on different levels:

- On the first levels, the context being very important, especially with
the absence of quotation marks for strings, it is necessary to use an
automaton (with states and transitions) in order to color these levels.

- For the following levels, the context being less important, we can simply
locate keywords, and color them.


The final rules will be available in the `highlightingRules` folder
especially for tests and for the `syntaxModesRules.ts` file


## File roles ##

- `highlightingRules/highlighting-*.json` this file contains the final rules
that have been generated for syntax highlighting.

- `definition.py` definition of constants (space, start of line, etc...).

- `rules_automaton.py` definitions of the coloring automata for the first levels.

- `list_keywords.py` keyword lists for levels where context is no longer important.

- `rules_list.py` file that allows to generate the syntax coloring rules
from the file `list_keywords.py`

- `generate-rules-highlighting.py` This file generates the rules for each level,
and for each language, from the  `rules_automaton.py` and `rules_list.py`

## How to change the syntax coloring ? ##

- If you want to modify the syntax highlighting on a level lower than 3, you have
to modify the associated function which creates the highlighting automaton in
the file `rules_automaton.py`

- If you want to modify the syntax highlighting on the following levels, you have
to modify the `KEYWORDS` and `NUMBER` variables in the `list_keywords.py` file, at
the desired level.


## How to update the syntactic coloring? ##

- To regenerate the json files containing the regexes, it is the
`generate-rules-highlighting.py` file that you have to execute,
it will allow you to see in the `highlighting-*.json` files the new regexes

- If you want to see the changes in Hedy, you will also have to
regenerate the javascript. This is done by running the
`./build-tools/heroku/generate-typescript` file


