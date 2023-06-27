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

### Skipping Faulty Code
When the AST is scanned for invalid rules and actually contains an error, an exception is thrown. 
We catch the exception and transpile the code again but this time we allow 'invalid' code that we are going to skip.
If this also fails, we raise the original exception, if it succeeds, 
the error(s) will be caught by the source-mapper and therefore be mapped. 
We go through all the errors and transpile again without allowing 'invalid' code, we ultimately get the original exception per mapping.
This we return to the user along-side the partially functional code.


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

### Type System

Hedy has a rudimentary type system created to provide better error messages to end users. The
type system performs type inferring, type validation and lookup table enrichment before transpilation happens.
Note that if in the future the transpiler still does not require any of the lookup table enrichments done by the type
system, type validation and transpiling can run in parallel.

The type system requires as input a lookup table containing the names of all variable definitions, which it later
enriches with their inferred types. The supported types are `string`, `integer`, `float`, `list`, `boolean`, `input`,
`any` and `none`. The type `any` is used when types cannot be inferred and is ignored in all type validations. The type
`input` is a composite data type used to denote user input (retrieved through the `ask` and `input` commands), which
means `input` can be multiple types depending on the value the user enters. At the moment, the user input could be
interpreted as `string`, `integer` or `float`. The lookup table is also used by the transpiler to differentiate literals
from expressions, e.g. the literal 'text' vs a variable called 'text'. Because of that the lookup table does not contain
only variable definitions, but also all expressions that need to be escaped, e.g. variable access such as `animals[0]`.

The lookup table is created and enriched in two separate steps. The first traversal of the abstract syntax tree puts in
the lookup table the entries required by the transpiler along with a reference to the sub-tree needed to infer their 
type. For example, the line `a is 1` will add the following entry `{name: 'a', tree: {data='integer', children:['1']}}`
The second traversal of the abstract syntax tree is performed to infer the types of expressions, store the inferred 
types of variables in the lookup table, and perform type validation. If during the second step the type system 
encounters a variable with type that has not been inferred yet, it will use the tree stored in the lookup entry to infer
its type. Note that there are valid scenarios in which the lookup entries will be accessed before their type is inferred. 
This is the case with for loops:

    for i in 1 to 10
        print i

In the above case, `print i` is visited before the definition of i in the for loop. To mitigate the issue, the lookup
entry tree is used to infer the type of `i`. There is a guard against cyclic definitions, e.g. `b is b + 1`. 
