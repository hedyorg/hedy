Design
==============================

Architecture
------------

The global idea of Hedy is that we transpile Hedy code to Python code by adding syntactic elements when they are missing. In the code base, this works in steps:

1. Hedy code is parsed based on the relevant grammar, creating an AST. This is done using the open source Lark parser.
2. Validity of the code is checked with the IsValid() function
3. If the code is valid, it is transformed into Python with the relevant function.

This logic all resides in hedy.py.

Transpiling
------------

Transpiling Hedy is a stepwise process. Firstly the code is parsed using Lark, resulting in an AST. The AST is then scanned for invalid rules. If these appear in the tree, the Hedy program is invalid and an error message will be generated. Secondly, a lookup table with all variable names occuring in the program is extracted from the AST. Finally, the AST is transformed into Python by adding needed syntax such as brackets.


Design Goals
------------

The overarching goal of Hedy is to successively add syntactic complexity to a Python-like language, until novices have mastered Python itself. To reach that goal, Hedy follows these design principles:

1.  **Concepts are offered at least three times in different forms:**

    Research from writing education has shown that it is best to offer concept in different forms over a long period of
    time. Furthermore it has been shown that a word needs to be read 7
    times before it is stored in long-term
    memory .

2.  **The initial offering of a concept is the simplest form possible:**

    Previous research has shown that syntax can be confusing for
    novices. Early levels thus are as syntax-free as possible to lower cognitive load.

3.  **Only one aspect of a concept changes at a time:**

    In his paper on [the spiral approach Shneiderman](https://www.sciencedirect.com/science/article/pii/0360131577900082) argued for small steps in teaching programming, which we follow for Hedy too. This allows us to focus the full attention of the learner on the new     syntactic element.

4.  **Adding syntactic elements like brackets and colons is deferred to the latest moment possible:**

    Previous research in the computer
    science education domain has shown that operators such as == and : can be especially hard for novices. In a [study](https://www.felienne.com/archives/5947) with high-schoolers we found that that might be due to their pronunciation. Research from natural language acquisition also indicates that parentheses and the
    colon are among the latest element of punctuation that learners
    typically learn. Given the choice between
    colons and parenthesis and other elements like indentation, the
    latter are introduced first.

5.  **Learning new forms is interleaved between concepts as much as possible:**

    We know that *spaced repetition* is a
    good way of memorizing, and that it takes time to learn punctuation,
    so we give students as much opportunity as possible to work with
    concepts before syntax changes.

6.  **At every level it is possible to create simple but meaningful
    programs:**

    It is important for all learners to engage in meaningful
    activities. Our experience in teaching
    high-school students (and even university CS students) is that
    learning syntax is not always seen as a useful activity. Students
    experience a large discrepancy between the computer being smart, for
    example by being able to multiply 1,910 and 5,671 within seconds,
    while simultaneously not being able to add a missing colon
    independently. We anticipate that when the initial syntax is simple,
    allowing novices to create a fun and meaningful program, they will
    later have more motivation to learn the details of the syntax.


Technical Design
----------------

### Grammars

Every level of Hedy is essentially a new language which requires its own grammar. Due to the gradual nature of Hedy,
however, the grammar of each level is only slightly different from the grammar of the previous one. To avoid massive
duplication, grammar code in Hedy is organized in the following manner:

* A `level1.lark` file serving as a base grammar file.
* A `level[1-9+]-Additions.lark` file for every level. Each file describes **only** the grammar changes compared to the
previous level. *Addition* files can add new grammar rules or override existing ones.

To get the grammar of a concrete level, Hedy takes the grammar of level 1 and merges consecutively all the changes
specified in the *Addition* files until the required level is reached. The final merged grammars for all levels
are generated in the `/grammars-Total` folder.
