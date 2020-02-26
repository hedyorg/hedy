# hedy
Hedy is a gradual programming language aimed at teaching programming and teaching Python. It teaches using different levels. The first level kust offers printing and asking for input. This level is meant to introduce learners to the idea of a progamming language, and the environment.
From there, Hedy builds up to include more complex syntax and additional concepts.




Hedy Design Goals & Principles
==============================

Design Goals
------------

The overarching goal of Hedy is to successively add syntactic complexity
to a Python-like language, until novices have mastered Python itself. To
reach that goal, Hedy follows these design principles:

1.  **Concepts are offered in least three times in different
    forms**Research from writing
    education [@simon_langue_1973; @fayol_etude_1989] has shown that it
    is needed to offer concept in different forms over a long period of
    time. Furthermore it has been shown that a word needs to be read 7
    times before it is stored in long-term
    memory [@verhallen_woorden_1994].

2.  **The initial offering of a concept is the simplest form possible**
    Previous research has shown that syntax can be confusing for
    novices [@denny_understanding_2011; @stefik_empirical_2013]. We
    therefore want to keep the initial syntax free of as many keywords
    and operators as possible to lower cognitive load.

3.  **Only one aspect of a concept changes at a time** In his paper on
    the Spiral approach Shneidermann argued for minimal
    changes [@shneiderman_teaching_1977] which we follow for Hedy too.
    This allows us to focus the full attention of the learner on the new
    syntactic element.

4.  **Adding syntactic elements like brackets and colons is deferred to
    the latest moment possible** Previous research in the computer
    science education domain has shown that operators such as [`==`]{}
    and [`:`]{} can be especially hard for novices, and prevent their
    effective *vocalization* of code [@hermans_code_2018], which is
    known to be an aid in remembering [@swidan_effect_2019]. Research
    from natural language acquisition shows that parenthesis and the
    colon are among the latest element of punctuation that learners
    typically learn [@ferreiro_managing_1999]. Given the choice between
    colons and parenthesis and other elements like indentation, the
    latter are introduced first.

5.  **Learning new forms is interleaved between concepts as much as
    possible** We know that *spaced repetition* [@kang_spaced_2016] is a
    good way of memorizing, and that it takes time to learn punctuation,
    so we give students as much opportunity as possible to work with
    concepts before syntax changes.

6.  **At every level it is possible to create simple but meaningful
    programs** It is important for all learners to engage in meaningful
    activities [@brown_situated_1989]. Our experience in teaching
    high-school students (and even university CS students) is that
    learning syntax is not always seen as a useful activity. Students
    experience a large discrepancy between the computer being smart, for
    example by being able to multiply 1,910 and 5,671 within seconds,
    while simultaneously not being able to add a missing colon
    independently. We anticipate that when the initial syntax is simple,
    allowing novices to create a fun and meaningful program, they will
    later have more motivation to learn the details of the syntax.

