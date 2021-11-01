Levels
------

In its current form, Hedy consists of 10 different levels. The levels loosely
follow the lesson series [**Python in de klas**](http://pythonindeklas.nl/)
("Python in the classroom") in such a way that these existing lessons can be
executed with Hedy instead of with Python.

### Level 1: Printing and input

At the first level, students can firstly print text. For this, no
syntactic elements are needed other than the keyword [`print`]
followed by arbitrary text. Furthermore students can ask for
input of the user using the keyword [`ask`]. Here we decided to use
the keyword [`ask`] rather than [`input`] because it is more aligned
with what the role of the keyword is in the code than with what it
*does*. Input of a user can be repeated with [`echo`], so very simple
programs can be created in which a user is asked for a name or a
favorite animal, fulfilling Design Goal 6.

### Level 2: Variables with is

At the second level, variables are added to the syntax. Defining a
variable is done with the word [`is`] rather than the equals symbol
fulfilling Design Goal 3 and Design Goal 4. We also add the option to
create lists and retrieve elements, including random elements from lists
with [`at`]. Adding lists and especially adding the option to select a
random item from a list allows for the creation of more interesting
programs such as a guessing game, a story with random elements, which is
an assignment from [**Python in de klas**](http://pythonindeklas.nl/)
("Python in the classroom"), or a customized dice.

### Level 3: Quotation marks and types
In Level 3 the first syntactic element is introduced: the use of
quotation marks to distinguish between strings and text. In teaching
novices we have seen that this distinction can be confusing for a long
time, so offering it early might help to draw attention to the fact that
computers need information about the types of variables. This level is
thus an interesting combination of explaining syntax and explaining
programming concepts, which underlines their interdependency. The
variable syntax using [`is`] remains unchanged, meaning that learners
can now use both [`number is 12`] and [`name is Hedy`].

### Level 4: Selection with if and else flat

In Level 5, selection with the if statement is introduced, but the
syntax is 'flat', i.e. placed on one line, resembling a regular syntax
more:\
[`if name is print `]\
Else statements are also included, and are also placed on one line,
using the keyword [`else`]:\
[`if name is print else print `].

### Level 5: Calculations **(new: was level 6)**

In Level 5, students learn to calculate with variables, so addition,
multiplication, subtraction and division are introduced. While this
might seem like a simple step, our experience taught us that the use of
[`*`] for multiplication, rather than $\times$, and the use of a
period rather than a comma as decimal separator for non-US students is a
steep learning curve and should be treated as a separate learning goal.

### Level 6: Repetition with repeat x times **(new: was level 5)**

In working with non-English native Python novices. Research has found
the keyword [`for`] to be a confusing word for repetition, especially
because it sounds like the word 'four' [@hermans_code_2018]. For our
first simplest form, according to Design Goal 2, we opt to use
Quorum [@stefik_quorum_2017] syntax [`repeat x times`]. In this
initial form, like the if the syntax is placed on one line:\
[`repeat 5 times print `]

### Level 7: Code blocks with one level of nesting **(new)**

After Level 6, there is a clear need to 'move on', as the body of a loop
(and also that of an if) can only consist of one line, which limits the
possibilities of programs that users can create. We assume this
limitation will be a motivating factor for learners, rather than 'having
to learn' the block structure of Python, they are motivated by the
prospect of building larger and more interesting programs (Design Goal
6). The syntax of the loop remains otherwise unchanged as per Design
Goal 3, so the new form is:\

[`repeat 5 times`]\
[`print `]\
[`print `]\

### Level 8: Code blocks with mutliple levels of nesting **(new)**

To allow for enough interleaving of concepts (Design Goal 5), we defer
the introduction of syntax concepts for now, and focus on more conceptual
additions: the nesting of blocks. We know indentation is a hard concept
for students to learn, so this warrants its own level (Design Goal 3).

### Level 9: For syntax looping over list **(new)**

In level 9, learners the range syntax, looping over the values in a list with `for animal in animals`.
This allows the customization of stories, drawing and songs. 

### Level 10: For syntax with in range

Once blocks are sufficiently automatized, learners will see a more
Python-like form of the for loop, namely: [`for i in range 0 to 5`].
This allows for access to the loop variable [`i`] and this allows for
more interesting programs, such as counting to 10. As per Design Goal 3,
the change is made small, and to do so (following Design Goal 4),
brackets and colons are deferred to a later level, but indentation which
was learned in Level 7 remains.

See for a discussion of fruther levels: https://github.com/Felienne/hedy/discussions/903


Old Levels
------
Leaving this here for now while refactoring the level structure further.


### Level 10: Learning the colon

To make the step to full Python, learners will need to use the colon to
denote the beginning of a block, in both loops and conditionals. Because
blocks are already known, we can teach learners to use a colon before
every indentation, and have them practice that extensively.

### Level 11: Adding round brackets

Level 11 adds round brackets in [`print`], [`range`] and
[`input`]. As per Design Goal 4, these are added as late as possible.

### Level 12: Adding rectangular brackets

In level 12, learners encounter different types of brackets for the
first time, because it adds rectangular brackets for list access, which
up to now was done with the keyword [`at`], following Design Goal 2.

### Level 13: Booleans

In level 13, booleans are added. Learners encounter True and False and how to use them in if statements

### Level 14: And and or

In level 14, Learners learn about and and or in if statements.

### Level 15: Comments

In level 15, comments are introduced. The learner will now know how to comment code

### Level 16: Smaller and bigger

In level 16, Learners learn about < and > in preparation for while loops

### Level 17: While loops

In level 17, learners are introduced to the while loop. With the previous knowledge of booleans and < and >, learners
can make basic while loops.

### Level 18: Access specific value in list

In level 18, learners are shown how to get a specific value from a list. The code to access a specific
value has already been available for a while but there was no explanation yet how to access a specific
value.

### Level 19: Loop through all values in lists

In level 19, learners are shown how to loop through a list. The length() function is also introduced,
as it makes looping through a list easier. The code to loop through a list has already been available since
the for loop was introduced but there was no explanation yet how to loop through the list.


### Level 20: Change is to = and ==

In level 20, we introduce the = and ==. All variable assignments change is to =. All equality checks
turn into ==.

### Level 21: Introducing !=

In level 21, we introduce the != in the equality checks. This is introduced after the change to = and
== as to make it easier to understand when you already know the syntax for =.

### Level 22: Introducing <= and >=

In level 22, we introduce <= and >=. This is introduced after the change to = and
== as to make it easier to understand when you already know the syntax for =.
