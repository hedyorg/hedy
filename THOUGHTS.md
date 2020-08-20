Some thoughts about Hedy design
======================

This document contains some design decisions and corresponding thoughts for future reference.
It is mainly Felienne's internal monologue, but feel free to read along!

## General thoughts

### Fix or warn or break?

Several issues in code can be fixed, in fact this is one of the main benefits of Hedy I would say.
This does lead to the fact that decision need to be made for each case whether we silently fix, warn or break.
For example, starting a line with a space. Do we allow it? It is important for kids to realize at one point that in Python and thus in Hedy
spaces have meaning, and only have meaning at the beginning of a line. For now, this is a warning.
Same question could be asked for case sensitivity of keywords. Do we allow it, and add a level where we tell kids it is then no longer allowed?
I am still deciding.


## Thoughts per level

### Level 2

#### Use of spaces

In Level 2, print now needs one space:
```command: "print " (" " | text | punctuation | list_access)*  -> print```

This makes processing easier, but has as a down side that ```print``` without an argument does not parse and thus not get a nice
error message. This could be fixed by more complicated processing.

Also in Level 2, ```print hello     world!``` works, but prints "hello world!".
I am not sure I like this behaviour. On the one hand side, this is a nice extra reason why we want quotation marks, to be able to tell Hedy that you really want spaces.
On the other hand, it breaks the promise that we literally print what is behind the keyword print.

#### Punctuation

The level 2 grammar has a separate rule for punctuation: ? ! and .
This is the case because we want to be able to print variables followed by punctuation without a space:
For example this code:

`name is Felienne
print hello name!`

should result in "hello Felienne!" and not "hello Felienne !"

### Level 3

#### Quotes only in print

In Level 3, we introduce the use of quotation marks in the `print` statement. In `ask`, this is not needed. 
The reasoning for this is that `print` is a 'real' statement which will occur in Python too and we want to build up to that.
`ask` will be replaced by a function call later on and as such does not really need to be real.
I have heard form users this is confusing, which I understand! We might want to change this at one point, or 
provide a better error message to explain the different with `print`.
