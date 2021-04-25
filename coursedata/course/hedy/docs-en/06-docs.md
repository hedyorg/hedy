title: Instructions
level: 6
---
Level 6 has a lot of new commands that allow you to do maths in your programs.

The addition sign is an easy one, it’s just like maths: for example, `5 + 5`.

You can subtract by using the `-` as a minus sign: `5 - 5`.

The sign for multiplication is a slightly different, because there is no special multiplication sign on your keyboard (except maybe for the letter x). Check it out, it’s really not there! That’s why we use the star (or asterisk) that’s above the 8 on your keyboard: `5 * 5` means 5 times 5.

You can divide by using the slash, like so: `20 / 5`.

Here you’ll find a couple of exercises to do in level 6.

# Throwing dice!

In level 6 you can make the Pickomino dice again, but now you can also calculate how many points you’ve earned. In the game of Pickomino an earthworm counts as 5 points. Now you can let Hedy throw the dice and calculate how many points you’ve thrown.
These are the steps for one die:

1 `choices is 1, 2, 3, 4, 5, earthworm`

2 `points is 0`

3 `throw is choices at random`

4 `print 'you have thrown ' throw`

5 `if throw is earthworm points is points + 5 else points is points + throw`

6 `print 'that makes ' points 'points' `

Now Hedy tells you the amount of points for one throw. Can you make a program in which Hedy tells you the total amount for 8 dice?

# Practice your tables of multiplication

Now that you can do maths with Hedy, you can also make a program to practice your tables of multiplications. You can come up with the exercises yourself, for example:

* `rightanswer is 11 * 27`
* `print 'What is 11 times 27?'`
* `answer is ask Do you know the answer?`
* `if answer is rightanswer print 'Good job!' else print 'Wrong! The answer is ' rightanswer`

You can also let the computer pick the numbers by using `random`.

In this way, you can simply choose a number of tables to practice, and from that you always get different calculations to practice:

* `tables is 4, 5, 6, 8`
* `times is 1, 2, 3, 4, 5, 6, 7, 8, 9, 10`

* `tablenumber is tables at random`
* `timesnumber is times at random`
* `rightanswer is tablenumber * timesnumber`

* `print 'What is ' tablenumber ' times ' timesnumber`

* `answer is ask What is the answer?`
* `if answer is rightanswer print 'Good job!' else print 'Wrong! The answer is ' rightanswer`

# Who is doing the dishes, and is that fair?

How many times does each person do the dishes? And is that fair? Now you can keep count.

1 `people is mum, pad, Emma, Sophie`

2  `emmasturn is 0`

3 `dishwasher is people at random`

4 `print dishwasher 'has to do the dishes!'

5 `if dishwasher is Emma emmasturn is emmasturn + 1`

6 `print 'This week it was Emma s turn ' emmasturn ' time(s)'`

Now you can copy lines 3 to 5 a couple of times, for example 7 times for a whole week.

# Sing a song with numbers in it

Childrens’ songs often contain a lot of repetition and sometimes numbers as well. An example is the American children’s song called 99 bottles of beer on the wall.

1 `verse is 99`

2 `print verse  'bottles of beer on the wall'`

3 `print verse 'bottles of beer'`

4 `print 'You take one down, pass it around'`

5 `verse is verse - 1`
6 `repeat 2 times print verse 'bottles of beer on the wall'`

7 `print verse 'bottles of beer'`

8 `print 'You take one down, pass it around'`

You can copy lines 6-8 and paste them under your program to keep the song going! Can you reach 0?

# That’s a lot of copy and paste

In Level 5 you’ve learned to repeat one line, for example:

* `repeat 3 times print 'Baby Shark Tutududududu'`

But as you can see in the 99 bottles of beer song, sometimes you want to repeat a couple of lines together instead of one single line. You can alway use copy and paste, but that’s a lot of work. In level 7 you’ll learn an easier way to repeat multiple lines!
