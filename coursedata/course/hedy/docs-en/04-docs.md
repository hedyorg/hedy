title: Instructions
level: 4
---
Level 4 uses the same rules for `ask` and `print`. You still need to use the quotation marks when you want to print something. Level 4 also introduces a new command: `if`.

Here you’ll find a couple of exercises to do in level 4.

# Siblings not allowed!

When I was learning to code, the first program I made was a program to check if my little sister was secretly using my computer. You can make a program like that in Hedy too. It goes like this:

* `name is ask Who are you?`
* `if name is Felienne print 'ok you can use the computer' else print 'access denied for you!'`

This code checks if the name that’s being typed in is exactly ‘Felienne’. If the name is ‘Felienne’, then Hedy prints the nice welcome message, if not Hedy will pront the second message.
Mind that Hedy is checking the name very precisely, it has to be exactly right, including the uppercase letter.

# Rock, paper, scissors

In Level 4 we can make a new game of rock paper scissors that you can actually play against the computer.  We have already written down the first lines of code for you, can you finish the code yourself?

* `yourpick is ask what do you choose?`
* `options is rock, paper, scissors`
* `computerpick is options at random`
* `if computerpick is scissors and yourpick is paper print 'the computer wins'`
* `if computerpick is scissors and yourpick is steen print 'you win'`

# Recreate dice
In level 4 you can make your own dice and use `if`. Like this:

* `choices is 1, 2, 3, 4, 5, earthworm`
* `throw is choices at random`
* `print 'you have thrown ' throw'`
* `if throw is earthworm print 'You dont have to throw again.' else print 'Try again!'`

Of course you can also make different dice from different games!

# Who is doing the dishes?
Your dishwashing code can be improved with `if` too, for example like this:

* `people is mum, dad, Emma, Sophie`
* `dishwasher is people at random`
* `if dishwasher is Sophie print 'Oh no! I have to do the dishes' else print 'Great! I dont have to do the dishes, because ' dishwasher ' has to! '`

# A better story

You could also improve your story with if, because you could program different endings to your story.

## Example

Make a story with two different endings, like this:

* The princess was walking through the forest
* She sees a scary monster

Happy ending:

* She takes out her sword and the monsters quickly runs away

Sad ending:

* The monster gobbles up the princess

## Assignment

Your turn!

1. Write a story with two different endings.

## Example Hedy code

* `print 'The princess was walking through the forest'`
* `print 'She sees a scary monster'`
* `ending is ask Do you want a happy or a sad ending?`
* `if ending is happy print 'She takes out her sword and the monster quickly runs away' else print 'The monster gobbles up the princess'`

## An interactive story

Just like in the previous levels, you can code that the player can choose the main character’s name. You can combine that with the if command and create a great interactive story!

## Repetition in your game or story

Unfortunately, you can only throw one die at the time, or pick one person to do the dishes. You might want to use multiple dice in your game, or make a schedule for doing the dishes for the whole week! In level 5 you’ll learn how to repeat a line in your code.
