# Adventures for Hedy Functions
## Level 11
### Introduction to functions
```
We can use something called functions now! They help us organize pieces of code that we can use again and again.

To create a function, use <code>{define}</code> and give it a name. The indented lines following it will be part of the function.

Then, whenever we need that code, we just use <code>{call}</code> with the function's name to call it up!

The example creates a function that will print a random fruit each time it is executed. Try it out!

<pre>{define} name_a_fruit
    fruits {is} "apples", "pears", "bananas", "kiwis", "grapes", "Oranges", "Mangoes", "Watermelon", "Cherries"
    {print} fruits {at} {random}

{print} "Today I will eat:"
{call} name_a_fruit

{print} "Tomorrow I will eat:"
{call} name_a_fruit

{repeat} 3 {times}
    {print} "The day after that I will eat:"
    {call} name_a_fruit
</pre>
```

### Turtle using Functions
```
With functions, we can make more organized code.
This code defines some functions to make it easier to draw shapes.

<pre>
{define} up
    {forward} 30

{define} down
    {turn} 180
    {forward} 30
    {turn} 180

{define} left
    {turn} -90
    {forward} 30
    {turn} 90
    
{define} right
    {turn} 90
    {forward} 30
    {turn} -90

{call} up
{call} left
{call} down
</pre>
```

## Level 12
### Intro
```
From this level onwards, functions can take special inputs called <i>arguments</i>. These <i>arguments</i> help the function do different things depending on what we put in. But we need to remember that changing <i>arguments</i> inside a function only affects what happens inside the function, not outside of it.

Use <code>{with}</code> and <code>{using}</code> with the <code>{define}</code> and <code>{call}</code> keywords.

The example function takes three <i>arguments</i> and prints the sum.

<pre>
{define} sum_of_three {using} a, b, c
    sum {is} a + b + c
    {print} a " + " b " + " c " = " sum
    
user_input {is} {ask} "Choose a number"
numbers {is} 1.1, 2.2, 3.3, 4.4, 5.5
number {is} numbers {at} {random}
{call} sum_of_three {with} 10, number, user_input
</pre>
```

## Level 14
### Intro
```
Functions can also give us something back, called a return value. We tell the function to give something back using the <code>{return}</code> keyword. The returned value can be assigned to a variable, used in a print statement, and in other ways. Experiment to find out!

The example defines a function which takes one <i>argument</i> and returns its square.

<pre>
{define} square {using} a
    {return} a * a
    
number {is} 7

{print} number " squared is " {call} square {with} number
</pre>
```