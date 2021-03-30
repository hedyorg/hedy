title: Instructions
level: 3
---
Mind that there are new rules in level 3! If you want to literally print the text you have to use quotation marks.

# Fix the name problem
In Level 2 we weren’t able to print the word name, because we already used it.
This code:

* `name is Hedy`
* `print so your name is name`

Prints in Level 2 "So your Hedy is Hedy"
In level 3 we can fix it by putting quotation marks around the text that you want to print literally. Try it!

# Rock, paper, scissors
In Level 3 we can also make the game of rock, paper, scissors. If you want to add text to your game, you’ll have to put it in quotation marks.

* `choices is rock, paper, scissors`
* `print 'The winner is ' choices at random`

# Make your own dice
Level 3 also allows you to make dice. In level 3 you can make sentences that include the amount that you’ve thrown.
This is the Pickamino dice again, but now with a nice sentence.

* `choices is 1, 2, 3, 4, 5, earthworm`
* `print 'You have thrown ' choices at random

Your turn to make some nice dice!

# Who is doing the dishes tonight?
Your code for doing the dishes can be upgraded too in level 3.

It looks like this:

* `people is mom, dad, Emma, Sophie`
* `print 'This person has to do the dishes tonight: ' people at random`

# A better story
You can improve your story in level 3, because you can use the word ‘name’ in your text (as long as you put it in quotation marks).

##Example
This is my story. The name that you choose for the main character will replace the word name. Pay close attention: All the sentences have to be in quotation marks, except the word name!

* the name of my main character is name
* name is walking through the forest
* name is a bit scared
* everywhere around him are strange noises
* name is afraid this is a haunted forest

## Assignment

Your turn!

1. Write a short story about your main character.
2. Write `name` instead of your main character’s name (like the example)
3. You’re also allowed to use sentences without `name`
4. Translate your story to Hedy code, like this:

Line 1: type: `name is` followed by your main character’s name.
For the following lines:
Type `print` followed by the sentence you came up with, but pay cose attention! The word name shouldn’t be in quotation marks if you want it to change into the main character’s name. Everything else should be in quotation marks after `print`.

## Example Hedy code
* `name is John`
* `print 'The name of my main character is `name
* `print name ' is walking through the forest'`
* `print name ' is a vit scared'`
* `print 'Everywhere around him ' name ' is hearing strange noises'`
* `print name ' is afraid this forest is haunted'`

## An interactive story
Make the story interactive by asking the main character’s name in the first line. Change `name is John` into `name is ask Who is the main character?`
This way you can pick a different name every time without having to change your code!

## Choices in your story or game
It would be really great if your story could be more interactive. For example, if you could choose whether there is a monster in your story or not. Or if you could see who the winner is of rock, paper, scissors. You can learn to program these things in level 4!
