Some thoughts about Hedy design
======================

In this document I am noting down some design decisions and corresponding thoughts for future reference.

Level 2
------------
In Level 2, print now needs one space:
command: "print " (" " | text | punctuation | list_access)*  -> print

This makes processing easier, but has as a down side that ```print``` without an argument does not parse and thus not get a nice
error message. This could be fixed by more complicated processing.
