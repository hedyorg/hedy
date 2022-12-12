Levels
------

In its current form, Hedy consists of 18 different levels. The levels loosely
follow the lesson series [**Python in de klas**](http://pythonindeklas.nl/)
("Python in the classroom") in such a way that these existing lessons can be
executed with Hedy instead of with Python.

### Level 1: Printing and input

At the first level, students can firstly print text. For this, no
syntactic elements are needed other than the keyword `print`
followed by arbitrary text. Furthermore students can ask for
input of the user using the keyword `ask`. Here we decided to use
the keyword `ask` rather than `input` because it is more aligned
with what the role of the keyword is in the code than with what it
*does*. Input of a user can be repeated with `echo`, so very simple
programs can be created in which a user is asked for a name or a
favorite animal, fulfilling Design Goal 6.

### Level 2: (Singular) variables with is

At the second level, variables are added to the syntax. Defining a variable is done with the word `is` rather than the equals symbol fulfilling Design Goal 3 and Design Goal 4. 

### Level 3: Lists with is
In level 3 we add the option to create lists and retrieve elements, including random elements from lists with `at`. Adding lists and especially adding the option to select a
random item from a list allows for the creation of more interesting programs such as a guessing game or a story with random elements, which is an assignment from [**Python in de klas**](http://pythonindeklas.nl/) ("Python in the classroom"), or a customized dice.
Level 3 also allows learners to add and remove lists elements with a textual syntax: `add animal to animals`.

### Level 4: Quotation marks and types
In Level 3 the first syntactic element is introduced: the use of quotation marks to distinguish between strings and text. In teaching novices we have seen that this distinction can be confusing for a long time, so offering it early might help to draw attention to the fact that
computers need information about the types of variables. This level is thus an interesting combination of explaining syntax and explaining
programming concepts, which underlines their interdependency. The variable syntax using `is` remains unchanged, meaning that learners
can now use both `number is 12` and `name is Hedy`.

### Level 5: Selection with if (pressed) and else flat

In Level 5, selection with the if statement is introduced, but the
syntax is 'flat', i.e. placed on one line, resembling a regular syntax
more:\
`if name is print `\
Another feature is the `if pressed` statement, making it possible to link commands
to any a-z and 1-0 key on the keyboard:\
`if x is pressed print `
Else statements are also included, and are also placed on one line,
using the keyword `else`:\
`if name is print else print `.
this also works together with `pressed`.

### Level 6: Calculations

In Level 6, students learn to calculate with variables. Therefore addition,
multiplication, subtraction and division are introduced. While this
might seem like a simple step, our experience taught us that the use of
`*` for multiplication, rather than `x` is a
steep learning curve and should be treated as a separate learning goal.

### Level 7: Repetition with repeat x times

In working with non-English native Python novices. Research has found
the keyword `for` to be a confusing word for repetition, especially
because it sounds like the word 'four'. For our
first simplest form, according to Design Goal 2, we opt to use
[Quorum](https://quorumlanguage.com/) syntax `repeat x times`. In this
initial form, like the if the syntax is placed on one line:\
`repeat 5 times print `
Repeat can also be used in combination with `pressed`, so that the program will
a keypress multiple times before terminating. 

### Level 8: Code blocks with one level of nesting 

After Level 7, there is a clear need to 'move on', since the body of a loop
(and also that of an `if`) can only consist of one line, which limits the
possibilities of programs that users can create. We assume this
limitation will be a motivating factor for learners, rather than 'having
to learn' the block structure of Python, they are motivated by the
prospect of building larger and more interesting programs (Design Goal
6). The syntax of the loop remains otherwise unchanged as per Design
Goal 3, so the new form is:\

```
repeat 5 times
  print 'Hello'
  print 'I am repeated 5 times'
```

### Level 9: Code blocks with multiple levels of nesting 

To allow for enough interleaving of concepts (Design Goal 5), we defer
the introduction of syntax concepts for now, and focus on more conceptual
additions: the nesting of blocks. We know indentation is a hard concept
for students to learn, so this warrants its own level (Design Goal 3).

### Level 10: For syntax looping over list 

In level 10, learners the `for` syntax to loop over the values in a list with `for animal in animals`.
This allows the customization of stories, drawing and songs. 

### Level 11: For syntax with in range

Once blocks are sufficiently automatized, learners will see a more
Python-like form of the for loop, namely: `for i in range 0 to 5`.
This allows for access to the loop variable `i` and this allows for
more interesting programs, such as counting to 10. As per Design Goal 3,
the change is made small, and to do so (following Design Goal 4),
brackets and colons are deferred to a later level, but indentation which
was introduced in Level 8 remains.

### Level 12: Datatypes

Learners are now allowed to use floats and need to place quotation marks around
strings to distinguish them from numbers.

### Level 13: And and or

In level 13, Learners learn about `and` and `or` in `if` statements.

### Level 14: Smaller and bigger

In level 14, Learners learn about `<(=)` and `>(=)` in preparation for while loops. 

### Level 15: While loops

In level 15, learners are introduced to the while loop. With the previous knowledge of loops and `<=` and `>=`, learners can make basic while loops.

### Level 16: Adding rectangular brackets

In this level, learners encounter brackets for the first time, because it adds rectangular brackets for list access, which up to now was done with the keyword `at`, following Design Goal 2. THis level also explain accessing lists with a numeric index, starting at 1. The code to access a specific
value has already been available technically since level 2, but there was no explanation yet how to access a specific value and it is not used in examples (and should maybe be removed?)

### Level 17: Learning elif and the colon

To make the step to full Python, learners will need to use the colon to denote the beginning of a block, in both loops and conditionals. 
Because blocks are already known and practiced over several levels, we can teach learners to use a colon before every indentation.

This level also introduces `elif` to allow for more exciting programs, since just adding a colon does not really create engagement.

### Level 18: Adding round brackets

Level 18 adds round brackets in `print` and `range` and changes `ask` to `input`. As per Design Goal 4, these are added as late as possible.


Additional features
------
### Comments

All levels allow for the use of comments, and it is up the the teachers to explain their different uses.
