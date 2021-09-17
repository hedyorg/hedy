# Semantics

This page is a first try at describing the semantics of Hedy. Because Hedy code is transpiled into Python, we define the semantics of an Hedy program in terms of the semantics of the resulting Python code, or, 
in case of an error, the resulting HedyException.

## Level 1

### Commands

Level 1 supports:
* `print`
* `ask`
* `forward`
* `turn`
* `echo`

#### Correct Programs


| Hedy     | Python     |
|----------|------------|
| print x  | print('x') |
| forward  | t.forward(50) |
| turn     | t.right(90) |
| ask x    | answer = input('x') |
| ask x    | answer = input('x') |
| echo y   | print('y', answer) |
 

#### Incorrect Programs

print -> Incomplete Exception
ask -> Incomplete Exception
echo -> Incomplete Exception

word other than print, ask, forward, turn, echo -> Invaid Exception


