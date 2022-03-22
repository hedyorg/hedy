# Semantics

This page is a first try at describing the semantics of Hedy. Because Hedy code is transpiled into Python, we define the semantics of an Hedy program in terms of the semantics of the resulting Python code, or, 
in case of an error, the resulting HedyException.

## Level 1

### Commands and types

Level 1 supports:

<table>
<thead>
  <tr>
    <th>Command</th>
    <th>Types</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td>print</td>
    <td>string</td>
  </tr>
  <tr>
    <td>ask</td>
    <td>string</td>
  </tr>
  <tr>
    <td>forward</td>
    <td>integer | empty</td>
  </tr>
  <tr>
    <td>turn</td>
    <td>'right' | 'left' | empty</td>
  </tr>
  <tr>
    <td>echo</td>
    <td>string | empty</td>
  </tr>
</tbody>
</table>


#### Correct Programs

<table>
<thead>
  <tr>
    <th>Hedy</th>
    <th>Python</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td>print x y</td>
    <td>print('x y')</td>
  </tr>
  <tr>
    <td>forward</td>
    <td>t = turtle.Turtle()<br>t.forward(50)</td>
  </tr>
  <tr>
    <td>forward 100</td>
    <td>t = turtle.Turtle()<br>t.forward(100)</td>
  </tr>
  <tr>
    <td>turn</td>
    <td>t = turtle.Turtle()<br>t.right(90)</td>
  </tr>
  <tr>
    <td>turn left</td>
    <td>t = turtle.Turtle()<br>t.left(90)</td>
  </tr>
  <tr>
    <td>turn right</td>
    <td>t = turtle.Turtle()<br>t.right(90)</td>
  </tr>
  <tr>
    <td>ask x</td>
    <td>answer = input('x')</td>
  </tr>
  <tr>
    <td>ask x<br>echo y</td>
    <td>answer = input('x')<br>print('y', answer)</td>
  </tr>
</tbody>
</table>


#### Incorrect Programs

<table>
<thead>
  <tr>
    <th>Hedy</th>
    <th>Exception</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td>print</td>
    <td>Incomplete Exception</td>
  </tr>
  <tr>
    <td>ask</td>
    <td>Incomplete Exception</td>
  </tr>
  <tr>
    <td>(forward | turn) text</td>
    <td>Invalid Argument Type Exception</td>
  </tr>
  <tr>
    <td>(not (print | ask | forward | turn | echo)) (any text)?</td>
    <td>Invalid Exception</td>
  </tr>
  <tr>
    <td>any valid line(s) of code not using ask<br>echo x</td>
    <td>Lonely Echo</td>
  </tr>
  <tr>
    <td>_SPACE (print | ask | forward | turn | echo) (any text)?</td>
    <td>Invalid space</td>
  </tr>
</tbody>
</table>

## Level 2

### Commands and types

Level 2 supports:

<table>
<thead>
  <tr>
    <th>Command</th>
    <th>Types</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td>print</td>
    <td>string | input</td>
  </tr>
  <tr>
    <td>ask*</td>
    <td>string | input</td>
  </tr>
  <tr>
    <td>forward</td>
    <td>integer | empty | input</td>
  </tr>
  <tr>
    <td>turn</td>
    <td>integer | empty | input</td>
  </tr>
  <tr>
    <td>is</td>
    <td>string (before `is`) + string (after `is`)</td>
  </tr>
    <tr>
    <td>sleep</td>
    <td>empty | integer</td>
  </tr>
</tbody>
</table>

* \* From this level on, we have to use `ask` in combination with `is`, so we get `<variablename> is ask <outputquestion>`. This way, the answer of the user will be stored in a variable.


#### Correct Programs

<table>
<thead>
  <tr>
    <th>Hedy</th>
    <th>Python</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td>print x y</td>
    <td>print('x y')</td>
  </tr>
  <tr>
    <td>forward</td>
    <td>t = turtle.Turtle()<br>t.forward(50)</td>
  </tr>
  <tr>
    <td>forward 100</td>
    <td>t = turtle.Turtle()<br>t.forward(100)</td>
  </tr>
  <tr>
    <td>a is 50<br/>forward a</td>
    <td>a = '50'<br/>t = turtle.Turtle()<br>t.forward(a)</td>
  </tr>
  <tr>
    <td>turn</td>
    <td>t = turtle.Turtle()<br>t.right(90)</td>
  </tr>
  <tr>
    <td>turn 100</td>
    <td>t = turtle.Turtle()<br>t.right(100)</td>
  </tr>
  <tr>
    <td>a is 50<br/>turn a</td>
    <td>a = '50'<br/>t = turtle.Turtle()<br>t.right(a)</td>
  </tr>
  <tr>
    <td>x is 90<br>print x</td>
    <td>x = '90'<br>print(x)</td>
  </tr>
  <tr>
    <td>x is ask y<br>print x</td>
    <td>x = input('y')<br>print(x)</td>
  </tr>
  <tr>
    <td>sleep</td>
    <td>time.sleep(1)</td>
  </tr>
  <tr>
    <td>sleep 1</td>
    <td>time.sleep(1)</td>
  </tr>
</tbody>
</table>


#### Incorrect Programs

<table>
<thead>
  <tr>
    <th>Hedy</th>
    <th>Exception</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td>print</td>
    <td>Incomplete Exception</td>
  </tr>
  <tr>
    <td>ask</td>
    <td>Incomplete Exception</td>
  </tr>
  <tr>
    <td>(not (print | ask | forward | turn)) (any text) (not is) (any text)?</td>
    <td>Invalid Exception</td>
  </tr>
  <tr>
    <td>_SPACE (print | ask | forward | turn) (any text)?</td>
    <td>Invalid space</td>
  </tr>
  <tr>
    <td>_SPACE (any text) is (any text)?</td>
    <td>Invalid space</td>
  </tr>
  <tr>
    <td>(forward | turn) text</td>
    <td>Invalid Argument Type Exception</td>
  </tr>
  <tr>
    <td>a is text<br/>(forward | turn) a</td>
    <td>Invalid Argument Type Exception</td>
  </tr>
</tbody>
</table>

## Level 3

### Commands and types

Level 3 supports:

<table>
<thead>
  <tr>
    <th>Command</th>
    <th>Types</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td>print</td>
    <td>string | input</td>
  </tr>
  <tr>
    <td>ask*</td>
    <td>string | input</td>
  </tr>
  <tr>
    <td>forward</td>
    <td>integer | empty | input</td>
  </tr>
  <tr>
    <td>turn</td>
    <td>integer | empty | input</td>
  </tr>
  <tr>
    <td>is</td>
    <td>string (before `is`) + any (after `is`)</td>
  </tr>
    <tr>
    <td>sleep</td>
    <td>empty | integer</td>
  </tr>
  <tr>
    <td>at random</td>
    <td>list</td>
  </tr>
  <tr>
    <td>add to</td>
    <td>list</td>
  </tr>
  <tr>
    <td>remove from</td>
    <td>list</td>
  </tr>
</tbody>
</table>

* \* We have to use `ask` in combination with `is`, so we get `<variablename> is ask <outputquestion>`. This way, the answer of the user will be stored in a variable.


#### Correct Programs

<table>
<thead>
  <tr>
    <th>Hedy</th>
    <th>Python</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td>print x y</td>
    <td>print('x y')</td>
  </tr>
  <tr>
    <td>forward</td>
    <td>t = turtle.Turtle()<br>t.forward(50)</td>
  </tr>
  <tr>
    <td>forward 50</td>
    <td>t = turtle.Turtle()<br>t.forward(50)</td>
  </tr>
  <tr>
    <td>a is 50<br/>forward a</td>
    <td>a = '50'<br/>t = turtle.Turtle()<br>t.forward(a)</td>
  </tr>
  <tr>
    <td>turn</td>
    <td>t = turtle.Turtle()<br>t.right(90)</td>
  </tr>
  <tr>
    <td>turn 90</td>
    <td>t = turtle.Turtle()<br>t.right(90)</td>
  </tr>
  <tr>
    <td>a is 50<br/>turn a</td>
    <td>a = '50'<br/>t = turtle.Turtle()<br>t.right(a)</td>
  </tr>
  <tr>
    <td>sleep</td>
    <td>time.sleep(1)</td>
  </tr>
  <tr>
    <td>sleep 1</td>
    <td>time.sleep(1)</td>
  </tr>
  <tr>
    <td>ask x</td>
    <td>answer = input('x')</td>
  </tr>
  <tr>
    <td>x is ask y<br>print x</td>
    <td>x = input('y')<br>print(x)</td>
  </tr>
  <tr>
    <td>x is a, b, c<br>(turn | forward) x at random</td>
    <td>x = ['a', 'b', 'c']<br>t = turtle.Turtle()<br>t.right(random.choice(x))</td>
  </tr>
  <tr>
    <td>x is a, b, c<br>print x at random</td>
    <td>x = ['a', 'b', 'c']<br>print(random.choice(x))</td>
  </tr>
  <tr>
    <td>a is 1, 2, 3<br/>f is 4<br/>add f to a</td>
    <td>a = ['1', '2', '3']<br/>f = '4'<br/>a.append(f)</td>
  </tr>
  <tr>
    <td>a is 1, 2, 3<br/>f is 4<br/>remove f from a</td>
    <td>a = ['1', '2', '3']<br/>f = '4'<br/>try:<br/>&emsp;&emsp;a.remove(f)<br/>except:<br/>&emsp;&emsp;pass</td>
  </tr>
</tbody>
</table>


#### Incorrect Programs

<table>
<thead>
  <tr>
    <th>Hedy</th>
    <th>Exception</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td>print</td>
    <td>Incomplete Exception</td>
  </tr>
  <tr>
    <td>ask</td>
    <td>Incomplete Exception</td>
  </tr>
  <tr>
    <td>(not (print | ask | forward | turn)) (any text) (not is) (any text)?</td>
    <td>Invalid Exception</td>
  </tr>
  <tr>
    <td>_SPACE (print | ask | forward | turn) (any text)?</td>
    <td>Invalid space</td>
  </tr>
  <tr>
    <td>_SPACE (any text) is (any text)?</td>
    <td>Invalid space</td>
  </tr>
 <tr>
    <td>(forward | turn) text</td>
    <td>Invalid Argument Type Exception</td>
  </tr>
  <tr>
    <td>a is text<br/>(forward | turn) a</td>
    <td>Invalid Argument Type Exception</td>
  </tr>
  <tr>
    <td>a is 1, 2, 3<br/>(forward | turn) a</td>
    <td>Invalid Argument Type Exception</td>
  </tr>
  <tr>
    <td>a is 1, 2, 3<br/>f is 4<br/>(add | remove) a (to | from) f</td>
    <td>Invalid Argument Type Exception</td>
  </tr>
  <tr>
    <td>items is 1, 2, 3<br/>print items</td>
    <td>Invalid Argument Type Exception</td>
  </tr>
  <tr>
    <td>items is (text without a comma)<br/>print items at random</td>
    <td>Invalid Argument Type Exception</td>
  </tr>
</tbody>
</table>

## Level 4

### Commands and types

Level 4 supports:

<table>
<thead>
  <tr>
    <th>Command</th>
    <th>Types</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td>print</td>
    <td>integer | string | input</td>
  </tr>
  <tr>
    <td>ask*</td>
    <td>integer | string | input</td>
  </tr>
  <tr>
    <td>forward</td>
    <td>integer | empty | input</td>
  </tr>
  <tr>
    <td>turn</td>
    <td>integer | empty | input</td>
  </tr>
  <tr>
    <td>is</td>
    <td>string (before `is`) + any (after `is`)</td>
  </tr>
  <tr>
    <td>sleep</td>
    <td>empty | integer</td>
  </tr>
  <tr>
    <td>at random</td>
    <td>list</td>
  </tr>
  <tr>
    <td>add to</td>
    <td>list</td>
  </tr>
  <tr>
    <td>remove from</td>
    <td>list</td>
  </tr>
</tbody>
</table>

* \* We have to use `ask` in combination with `is`, so we get `<variablename> is ask <outputquestion>`. This way, the answer of the user will be stored in a variable.



#### Correct Programs

<table>
<thead>
  <tr>
    <th>Hedy</th>
    <th>Python</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td>print 'x' 'y'</td>
    <td>print('xy')</td>
  </tr>
  <tr>
    <td>forward</td>
    <td>t = turtle.Turtle()<br>t.forward(50)</td>
  </tr>
  <tr>
    <td>forward 50</td>
    <td>t = turtle.Turtle()<br>t.forward(50)</td>
  </tr>
  <tr>
    <td>a is 50<br/>forward a</td>
    <td>a = '50'<br/>t = turtle.Turtle()<br>t.forward(a)</td>
  </tr>
  <tr>
    <td>turn</td>
    <td>t = turtle.Turtle()<br>t.right(90)</td>
  </tr>
  <tr>
    <td>turn 90</td>
    <td>t = turtle.Turtle()<br>t.right(90)</td>
  </tr>
  <tr>
    <td>a is 50<br/>turn a</td>
    <td>a = '50'<br/>t = turtle.Turtle()<br>t.right(a)</td>
  </tr>
  <tr>
    <td>sleep</td>
    <td>time.sleep(1)</td>
  </tr>
  <tr>
    <td>sleep 1</td>
    <td>time.sleep(1)</td>
  </tr>
  <tr>
    <td>x is ask 'y'<br>print x</td>
    <td>x = input('y')<br>print(x)</td>
  </tr>
  <tr>
    <td>x is a, b, c<br>print x at random</td>
    <td>x = ['a', 'b', 'c']<br>print(random.choice(x))</td>
  </tr>
  <tr>
    <td>a is 1, 2, 3<br/>f is 4<br/>add f to a</td>
    <td>a = ['1', '2', '3']<br/>f = '4'<br/>a.append(f)</td>
  </tr>
  <tr>
    <td>a is 1, 2, 3<br/>f is 4<br/>remove f from a</td>
    <td>a = ['1', '2', '3']<br/>f = '4'<br/>try:<br/>&emsp;&emsp;a.remove(f)<br/>except:<br/>&emsp;&emsp;pass</td>
  </tr>
</tbody>
</table>


#### Incorrect Programs

<table>
<thead>
  <tr>
    <th>Hedy</th>
    <th>Exception</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td>print</td>
    <td>Incomplete Exception</td>
  </tr>
  <tr>
    <td>ask</td>
    <td>Incomplete Exception</td>
  </tr>
    <tr>
    <td>(ask | print) (any text without quotes around it)</td>
    <td>Unquoted Text Exception</td>
  </tr>
  <tr>
    <td>(not (print | ask | forward | turn)) (any text) (not is) (any text)?</td>
    <td>Invalid Exception</td>
  </tr>
  <tr>
    <td>_SPACE (print | ask | forward | turn) (any text)?</td>
    <td>Invalid space</td>
  </tr>
  <tr>
    <td>_SPACE (any text) is (any text)?</td>
    <td>Invalid space</td>
  </tr>
  <tr>
    <td>a is 1, 2, 3<br/>answer is ask 'Is the number in ' a</td>
    <td>Invalid Argument Type Exception</td>
  </tr>  
  <tr>
    <td>(forward | turn) text</td>
    <td>Invalid Argument Type Exception</td>
  </tr>
  <tr>
    <td>a is text<br/>(forward | turn) a</td>
    <td>Invalid Argument Type Exception</td>
  </tr>
  <tr>
    <td>a is 1, 2, 3<br/>(forward | turn) a</td>
    <td>Invalid Argument Type Exception</td>
  </tr>
  <tr>
    <td>a is 1, 2, 3<br/>f is 4<br/>(add | remove) a (to | from) f</td>
    <td>Invalid Argument Type Exception</td>
  </tr>
  <tr>
    <td>items is 1, 2, 3<br/>print items</td>
    <td>Invalid Argument Type Exception</td>
  </tr>
  <tr>
    <td>items is (text without a comma)<br/>print items at random</td>
    <td>Invalid Argument Type Exception</td>
  </tr>
</tbody>
</table>

## Level 5

### Commands and types

Level 5 supports:

<table>
<thead>
  <tr>
    <th>Command</th>
    <th>Types</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td>print</td>
    <td>integer | string | input</td>
  </tr>
  <tr>
    <td>ask*</td>
    <td>integer | string | input</td>
  </tr>
  <tr>
    <td>forward</td>
    <td>integer | empty | input</td>
  </tr>
  <tr>
    <td>turn</td>
    <td>integer | empty | input</td>
  </tr>
  <tr>
    <td>is</td>
    <td>string (before `is`) + any (after `is`)</td>
  </tr>
  <tr>
    <td>sleep</td>
    <td>empty | integer</td>
  </tr>
  <tr>
    <td>at random</td>
    <td>list</td>
  </tr>
  <tr>
    <td>add to</td>
    <td>list</td>
  </tr>
  <tr>
    <td>remove from</td>
    <td>list</td>
  </tr>
  <tr>
    <td>if</td>
    <td>boolean</td>
  </tr>
  <tr>
    <td>if else</td>
    <td>boolean</td>
  </tr>
  <tr>
    <td>in</td>
    <td>any (before `in`) + list (after `in`)</td>
  </tr>
</tbody>
</table>

* \* We have to use `ask` in combination with `is`, so we get `<variablename> is ask <outputquestion>`. This way, the answer of the user will be stored in a variable.


#### Correct Programs

<table>
<thead>
  <tr>
    <th>Hedy</th>
    <th>Python</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td>print 'x' 'y'</td>
    <td>print('xy')</td>
  </tr>
  <tr>
    <td>forward</td>
    <td>t = turtle.Turtle()<br>t.forward(50)</td>
  </tr>
  <tr>
    <td>forward 50</td>
    <td>t = turtle.Turtle()<br>t.forward(50)</td>
  </tr>
  <tr>
    <td>a is 50<br/>forward a</td>
    <td>a = '50'<br/>t = turtle.Turtle()<br>t.forward(a)</td>
  </tr>
  <tr>
    <td>turn</td>
    <td>t = turtle.Turtle()<br>t.right(90)</td>
  </tr>
  <tr>
    <td>turn 90</td>
    <td>t = turtle.Turtle()<br>t.right(90)</td>
  </tr>
  <tr>
    <td>a is 50<br/>turn a</td>
    <td>a = '50'<br/>t = turtle.Turtle()<br>t.right(a)</td>
  </tr>
  <tr>
    <td>sleep</td>
    <td>time.sleep(1)</td>
  </tr>
  <tr>
    <td>sleep 1</td>
    <td>time.sleep(1)</td>
  </tr>
  <tr>
    <td>x is ask 'y'<br>print x</td>
    <td>x = input('y')<br>print(x)</td>
  </tr>
  <tr>
    <td>x is a, b, c<br>print x at random</td>
    <td>x = ['a', 'b', 'c']<br>print(random.choice(x))</td>
  </tr>
  <tr>
    <td>a is 1, 2, 3<br/>f is 4<br/>add f to a</td>
    <td>a = ['1', '2', '3']<br/>f = '4'<br/>a.append(f)</td>
  </tr>
  <tr>
    <td>a is 1, 2, 3<br/>f is 4<br/>remove f from a</td>
    <td>a = ['1', '2', '3']<br/>f = '4'<br/>try:<br/>&emsp;&emsp;a.remove(f)<br/>except:<br/>&emsp;&emsp;pass</td>
  </tr>
  <tr>
    <td>a is 1, 2, 3<br/>f is 4<br/>remove f from a</td>
    <td>a = ['1', '2', '3']<br/>f = '4'<br/>try:<br/>&emsp;&emsp;a.remove(f)<br/>except:<br/>&emsp;&emsp;pass</td>
  </tr>
  <tr>
    <td>name is Hedy<br/>if name is Hedy print 'great' else print 'fine'</td>
    <td>name = 'Hedy'<br/>if name == 'Hedy':<br/>&emsp;&emsp;print(f'great')<br/>else:<br/>&emsp;&emsp;print(f'fine')</td>
  </tr>
  <tr>
    <td>items is red, green<br/>selected is red<br/>if selected in items print 'found!'</td>
    <td>items = ['red', 'green']<br/>selected = 'red'<br/>if selected in items:<br/>&emsp;&emsp;print(f'found!')</td>
  </tr>
</tbody>
</table>


#### Incorrect Programs

<table>
<thead>
  <tr>
    <th>Hedy</th>
    <th>Exception</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td>print</td>
    <td>Incomplete Exception</td>
  </tr>
  <tr>
    <td>print'x'</td>
    <td>Invalid command</td>
  </tr>
  <tr>
    <td>ask</td>
    <td>Incomplete Exception</td>
  </tr>
    <tr>
    <td>(ask | print) (any text without quotes around it)</td>
    <td>Unquoted Text Exception</td>
  </tr>
  <tr>
    <td>(not (print | ask | forward | turn)) (any text) (not is) (any text)?</td>
    <td>Invalid Exception</td>
  </tr>
  <tr>
    <td>_SPACE (print | ask | forward | turn) (any text)?</td>
    <td>Invalid space</td>
  </tr>
  <tr>
    <td>_SPACE (any text) is (any text)?</td>
    <td>Invalid space</td>
  </tr>
  <tr>
    <td>a is 1, 2, 3<br/>answer is ask 'Is the number in ' a</td>
    <td>Invalid Argument Type Exception</td>
  </tr>  
  <tr>
    <td>(forward | turn) text</td>
    <td>Invalid Argument Type Exception</td>
  </tr>
  <tr>
    <td>a is text<br/>(forward | turn) a</td>
    <td>Invalid Argument Type Exception</td>
  </tr>
  <tr>
    <td>a is 1, 2, 3<br/>(forward | turn) a</td>
    <td>Invalid Argument Type Exception</td>
  </tr>
  <tr>
    <td>a is 1, 2, 3<br/>f is 4<br/>(add | remove) a (to | from) f</td>
    <td>Invalid Argument Type Exception</td>
  </tr>
  <tr>
    <td>items is 1, 2, 3<br/>print items</td>
    <td>Invalid Argument Type Exception</td>
  </tr>
  <tr>
    <td>a is 1 2<br/>one is 1<br/>if one in a print 'found!'</td>
    <td>Invalid Argument Type Exception</td>
  </tr>
  <tr>
    <td>name is 1, 2<br/>if '1' is name print 'found'</td>
    <td>Invalid Argument Type Exception</td>
  </tr>
</tbody>
</table>


## Level 6

### Commands and types

Level 6 supports:

<table>
<thead>
  <tr>
    <th>Command</th>
    <th>Types</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td>print</td>
    <td>integer | string | input</td>
  </tr>
  <tr>
    <td>ask*</td>
    <td>integer | string | input</td>
  </tr>
  <tr>
    <td>forward</td>
    <td>integer | empty | input</td>
  </tr>
  <tr>
    <td>turn</td>
    <td>integer | empty | input</td>
  </tr>
  <tr>
    <td>is</td>
    <td>string (before `is`) + any (after `is`)</td>
  </tr>
  <tr>
    <td>sleep</td>
    <td>empty | integer</td>
  </tr>
  <tr>
    <td>at random</td>
    <td>list</td>
  </tr>
  <tr>
    <td>add to</td>
    <td>list</td>
  </tr>
  <tr>
    <td>remove from</td>
    <td>list</td>
  </tr>
  <tr>
    <td>if</td>
    <td>boolean</td>
  </tr>
  <tr>
    <td>if else</td>
    <td>boolean</td>
  </tr>
  <tr>
    <td>in</td>
    <td>any (before `in`) + list (after `in`)</td>
  </tr>
</tbody>
</table>

* \* We have to use `ask` in combination with `is`, so we get `<variablename> is ask <outputquestion>`. This way, the answer of the user will be stored in a variable.


#### Correct Programs

<table>
<thead>
  <tr>
    <th>Hedy</th>
    <th>Python</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td>print 'x' 'y'</td>
    <td>print('xy')</td>
  </tr>
  <tr>
    <td>print 1 + 1</td>
    <td>print(f'{int(1) + int(1)}')</td>
  </tr>
  <tr>
    <td>print 1 - 1</td>
    <td>print(f'{int(1) - int(1)}')</td>
  </tr>
  <tr>
    <td>print 1 * 1</td>
    <td>print(f'{int(1) * int(1)}')</td>
  </tr>
  <tr>
    <td>print 1 / 1</td>
    <td>print(f'{int(1) / int(1)}')</td>
  </tr>
  <tr>
    <td>a is 1<br/>print a</td>
    <td>a = '1'<br/>print(f'{a}')</td>
  </tr>
  <tr>
    <td>forward</td>
    <td>t = turtle.Turtle()<br>t.forward(50)</td>
  </tr>
  <tr>
    <td>forward 50</td>
    <td>t = turtle.Turtle()<br>t.forward(50)</td>
  </tr>
  <tr>
    <td>a is 50<br/>forward a</td>
    <td>a = '50'<br/>t = turtle.Turtle()<br>t.forward(a)</td>
  </tr>
  <tr>
    <td>turn</td>
    <td>t = turtle.Turtle()<br>t.right(90)</td>
  </tr>
  <tr>
    <td>turn 90</td>
    <td>t = turtle.Turtle()<br>t.right(90)</td>
  </tr>
  <tr>
    <td>a is 50<br/>turn a</td>
    <td>a = '50'<br/>t = turtle.Turtle()<br>t.right(a)</td>
  </tr>
  <tr>
    <td>sleep</td>
    <td>time.sleep(1)</td>
  </tr>
  <tr>
    <td>sleep 1</td>
    <td>time.sleep(1)</td>
  </tr>
  <tr>
    <td>x is ask 'y'<br>print x</td>
    <td>x = input('y')<br>print(x)</td>
  </tr>
  <tr>
    <td>x is a, b, c<br>print x at random</td>
    <td>x = ['a', 'b', 'c']<br>print(random.choice(x))</td>
  </tr>
  <tr>
    <td>a is 1, 2, 3<br/>f is 4<br/>add f to a</td>
    <td>a = ['1', '2', '3']<br/>f = '4'<br/>a.append(f)</td>
  </tr>
  <tr>
    <td>a is 1, 2, 3<br/>f is 4<br/>remove f from a</td>
    <td>a = ['1', '2', '3']<br/>f = '4'<br/>try:<br/>&emsp;&emsp;a.remove(f)<br/>except:<br/>&emsp;&emsp;pass</td>
  </tr>
  <tr>
    <td>a is 1, 2, 3<br/>f is 4<br/>remove f from a</td>
    <td>a = ['1', '2', '3']<br/>f = '4'<br/>try:<br/>&emsp;&emsp;a.remove(f)<br/>except:<br/>&emsp;&emsp;pass</td>
  </tr>
  <tr>
    <td>name is Hedy<br/>if name is Hedy print 'great' else print 'fine'</td>
    <td>name = 'Hedy'<br/>if name == 'Hedy':<br/>&emsp;&emsp;print(f'great')<br/>else:<br/>&emsp;&emsp;print(f'fine')</td>
  </tr>
  <tr>
    <td>items is red, green<br/>selected is red<br/>if selected in items print 'found!'</td>
    <td>items = ['red', 'green']<br/>selected = 'red'<br/>if selected in items:<br/>&emsp;&emsp;print(f'found!')</td>
  </tr>
</tbody>
</table>


#### Incorrect Programs

<table>
<thead>
  <tr>
    <th>Hedy</th>
    <th>Exception</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td>print</td>
    <td>Incomplete Exception</td>
  </tr>
  <tr>
    <td>print'x'</td>
    <td>Invalid command</td>
  </tr>
  <tr>
    <td>print 1.0 + 1</td>
    <td>Unsupported decimal number</td>
  </tr>
  <tr>
    <td>print 1,0 + 1</td>
    <td>Unsupported decimal number</td>
  </tr>
  <tr>
    <td>ask</td>
    <td>Incomplete Exception</td>
  </tr>
    <tr>
    <td>(ask | print) (any text without quotes around it)</td>
    <td>Unquoted Text Exception</td>
  </tr>
  <tr>
    <td>(not (print | ask | forward | turn)) (any text) (not is) (any text)?</td>
    <td>Invalid Exception</td>
  </tr>
  <tr>
    <td>_SPACE (print | ask | forward | turn) (any text)?</td>
    <td>Invalid space</td>
  </tr>
  <tr>
    <td>_SPACE (any text) is (any text)?</td>
    <td>Invalid space</td>
  </tr>
  <tr>
    <td>a is 1, 2, 3<br/>answer is ask 'Is the number in ' a</td>
    <td>Invalid Argument Type Exception</td>
  </tr>  
  <tr>
    <td>(forward | turn) text</td>
    <td>Invalid Argument Type Exception</td>
  </tr>
  <tr>
    <td>a is text<br/>(forward | turn) a</td>
    <td>Invalid Argument Type Exception</td>
  </tr>
  <tr>
    <td>a is 1, 2, 3<br/>(forward | turn) a</td>
    <td>Invalid Argument Type Exception</td>
  </tr>
  <tr>
    <td>a is 1, 2, 3<br/>f is 4<br/>(add | remove) a (to | from) f</td>
    <td>Invalid Argument Type Exception</td>
  </tr>
  <tr>
    <td>items is 1, 2, 3<br/>print items</td>
    <td>Invalid Argument Type Exception</td>
  </tr>
  <tr>
    <td>a is 'test'<br/>print a + 1</td>
    <td>Invalid Argument Type Exception</td>
  </tr>
  <tr>
    <td>a is 'text'<br/>one is 1<br/>if one in a print 'found!'</td>
    <td>Invalid Argument Type Exception</td>
  </tr>
  <tr>
    <td>name is 1, 2<br/>if '1' is name print 'found'</td>
    <td>Invalid Argument Type Exception</td>
  </tr>
</tbody>
</table>

## Level 7

### Commands and types

Level 7 supports:

<table>
<thead>
  <tr>
    <th>Command</th>
    <th>Types</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td>print</td>
    <td>integer | string | input</td>
  </tr>
  <tr>
    <td>ask*</td>
    <td>integer | string | input</td>
  </tr>
  <tr>
    <td>forward</td>
    <td>integer | empty | input</td>
  </tr>
  <tr>
    <td>turn</td>
    <td>integer | empty | input</td>
  </tr>
  <tr>
    <td>is</td>
    <td>string (before `is`) + any (after `is`)</td>
  </tr>
  <tr>
    <td>sleep</td>
    <td>empty | integer</td>
  </tr>
  <tr>
    <td>at random</td>
    <td>list</td>
  </tr>
  <tr>
    <td>add to</td>
    <td>list</td>
  </tr>
  <tr>
    <td>remove from</td>
    <td>list</td>
  </tr>
  <tr>
    <td>if</td>
    <td>boolean</td>
  </tr>
  <tr>
    <td>if else</td>
    <td>boolean</td>
  </tr>
  <tr>
    <td>in</td>
    <td>any (before `in`) + list (after `in`)</td>
  </tr>
  <tr>
    <td>repeat</td>
    <td>integer + 'times' | input + 'times'</td>
  </tr>
</tbody>
</table>

* \* We have to use `ask` in combination with `is`, so we get `<variablename> is ask <outputquestion>`. This way, the answer of the user will be stored in a variable.



#### Correct Programs

<table>
<thead>
  <tr>
    <th>Hedy</th>
    <th>Python</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td>print 'x' 'y'</td>
    <td>print('xy')</td>
  </tr>
  <tr>
    <td>print 1 + 1</td>
    <td>print(f'{int(1) + int(1)}')</td>
  </tr>
  <tr>
    <td>print 1 - 1</td>
    <td>print(f'{int(1) - int(1)}')</td>
  </tr>
  <tr>
    <td>print 1 * 1</td>
    <td>print(f'{int(1) * int(1)}')</td>
  </tr>
  <tr>
    <td>print 1 / 1</td>
    <td>print(f'{int(1) / int(1)}')</td>
  </tr>
  <tr>
    <td>a is 1<br/>print a</td>
    <td>a = '1'<br/>print(f'{a}')</td>
  </tr>
  <tr>
    <td>forward</td>
    <td>t = turtle.Turtle()<br>t.forward(50)</td>
  </tr>
  <tr>
    <td>forward 50</td>
    <td>t = turtle.Turtle()<br>t.forward(50)</td>
  </tr>
  <tr>
    <td>a is 50<br/>forward a</td>
    <td>a = '50'<br/>t = turtle.Turtle()<br>t.forward(a)</td>
  </tr>
  <tr>
    <td>turn</td>
    <td>t = turtle.Turtle()<br>t.right(90)</td>
  </tr>
  <tr>
    <td>turn 90</td>
    <td>t = turtle.Turtle()<br>t.right(90)</td>
  </tr>
  <tr>
    <td>a is 50<br/>turn a</td>
    <td>a = '50'<br/>t = turtle.Turtle()<br>t.right(a)</td>
  </tr>
  <tr>
    <td>sleep</td>
    <td>time.sleep(1)</td>
  </tr>
  <tr>
    <td>sleep 1</td>
    <td>time.sleep(1)</td>
  </tr>
  <tr>
    <td>x is ask 'y'<br>print x</td>
    <td>x = input('y')<br>print(x)</td>
  </tr>
  <tr>
    <td>x is a, b, c<br>print x at random</td>
    <td>x = ['a', 'b', 'c']<br>print(random.choice(x))</td>
  </tr>
  <tr>
    <td>a is 1, 2, 3<br/>f is 4<br/>add f to a</td>
    <td>a = ['1', '2', '3']<br/>f = '4'<br/>a.append(f)</td>
  </tr>
  <tr>
    <td>a is 1, 2, 3<br/>f is 4<br/>remove f from a</td>
    <td>a = ['1', '2', '3']<br/>f = '4'<br/>try:<br/>&emsp;&emsp;a.remove(f)<br/>except:<br/>&emsp;&emsp;pass</td>
  </tr>
  <tr>
    <td>a is 1, 2, 3<br/>f is 4<br/>remove f from a</td>
    <td>a = ['1', '2', '3']<br/>f = '4'<br/>try:<br/>&emsp;&emsp;a.remove(f)<br/>except:<br/>&emsp;&emsp;pass</td>
  </tr>
  <tr>
    <td>name is Hedy<br/>if name is Hedy print 'great' else print 'fine'</td>
    <td>name = 'Hedy'<br/>if name == 'Hedy':<br/>&emsp;&emsp;print(f'great')<br/>else:<br/>&emsp;&emsp;print(f'fine')</td>
  </tr>
  <tr>
    <td>items is red, green<br/>selected is red<br/>if selected in items print 'found!'</td>
    <td>items = ['red', 'green']<br/>selected = 'red'<br/>if selected in items:<br/>&emsp;&emsp;print(f'found!')</td>
  </tr>
  <tr>
    <td>repeat 3 times print 'hello!'</td>
    <td>for i in range(int('3')):<br/>&emsp;&emsp;print(f'hello!')</td>
  </tr>
  <tr>
    <td>n is 3<br/>repeat n times print 'hello!'</td>
    <td>n = '3'<br/>for i in range(int(n)):<br/>&emsp;&emsp;print(f'hello!')</td>
  </tr>
</tbody>
</table>


#### Incorrect Programs

<table>
<thead>
  <tr>
    <th>Hedy</th>
    <th>Exception</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td>print</td>
    <td>Incomplete Exception</td>
  </tr>
  <tr>
    <td>print'x'</td>
    <td>Invalid command</td>
  </tr>
  <tr>
    <td>print 1.0 + 1</td>
    <td>Unsupported decimal number</td>
  </tr>
  <tr>
    <td>print 1,0 + 1</td>
    <td>Unsupported decimal number</td>
  </tr>
  <tr>
    <td>ask</td>
    <td>Incomplete Exception</td>
  </tr>
    <tr>
    <td>(ask | print) (any text without quotes around it)</td>
    <td>Unquoted Text Exception</td>
  </tr>
  <tr>
    <td>(not (print | ask | forward | turn)) (any text) (not is) (any text)?</td>
    <td>Invalid Exception</td>
  </tr>
  <tr>
    <td>_SPACE (print | ask | forward | turn) (any text)?</td>
    <td>Invalid space</td>
  </tr>
  <tr>
    <td>_SPACE (any text) is (any text)?</td>
    <td>Invalid space</td>
  </tr>
  <tr>
    <td>a is 1, 2, 3<br/>answer is ask 'Is the number in ' a</td>
    <td>Invalid Argument Type Exception</td>
  </tr>  
  <tr>
    <td>(forward | turn) text</td>
    <td>Invalid Argument Type Exception</td>
  </tr>
  <tr>
    <td>a is text<br/>(forward | turn) a</td>
    <td>Invalid Argument Type Exception</td>
  </tr>
  <tr>
    <td>a is 1, 2, 3<br/>(forward | turn) a</td>
    <td>Invalid Argument Type Exception</td>
  </tr>
  <tr>
    <td>a is 1, 2, 3<br/>f is 4<br/>(add | remove) a (to | from) f</td>
    <td>Invalid Argument Type Exception</td>
  </tr>
  <tr>
    <td>items is 1, 2, 3<br/>print items</td>
    <td>Invalid Argument Type Exception</td>
  </tr>
  <tr>
    <td>a is 'test'<br/>print a + 1</td>
    <td>Invalid Argument Type Exception</td>
  </tr>
  <tr>
    <td>a is 'text'<br/>one is 1<br/>if one in a print 'found!'</td>
    <td>Invalid Argument Type Exception</td>
  </tr>
  <tr>
    <td>name is 1, 2<br/>if '1' is name print 'found'</td>
    <td>Invalid Argument Type Exception</td>
  </tr>
</tbody>
</table>


## Level 8

### Commands

Level 8 supports:

<table>
<thead>
  <tr>
    <th>Command</th>
    <th>Types</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td>print</td>
    <td>integer | string | input</td>
  </tr>
  <tr>
    <td>ask*</td>
    <td>integer | string | input</td>
  </tr>
  <tr>
    <td>forward</td>
    <td>integer | empty | input</td>
  </tr>
  <tr>
    <td>turn</td>
    <td>integer | empty | input</td>
  </tr>
  <tr>
    <td>is</td>
    <td>string (before `is`) + any (after `is`)</td>
  </tr>
  <tr>
    <td>sleep</td>
    <td>empty | integer</td>
  </tr>
  <tr>
    <td>at random</td>
    <td>list</td>
  </tr>
  <tr>
    <td>add to</td>
    <td>list</td>
  </tr>
  <tr>
    <td>remove from</td>
    <td>list</td>
  </tr>
  <tr>
    <td>if</td>
    <td>boolean</td>
  </tr>
  <tr>
    <td>if else</td>
    <td>boolean</td>
  </tr>
  <tr>
    <td>in</td>
    <td>any (before `in`) + list (after `in`)</td>
  </tr>
  <tr>
    <td>repeat</td>
    <td>integer + 'times' | input + 'times'</td>
  </tr>
</tbody>
</table>

* \* We have to use `ask` in combination with `is`, so we get `<variablename> is ask <outputquestion>`. This way, the answer of the user will be stored in a variable.


#### Correct Programs

<table>
<thead>
  <tr>
    <th>Hedy</th>
    <th>Python</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td>print 'x' 'y'</td>
    <td>print('xy')</td>
  </tr>
  <tr>
    <td>print 1 + 1</td>
    <td>print(f'{int(1) + int(1)}')</td>
  </tr>
  <tr>
    <td>print 1 - 1</td>
    <td>print(f'{int(1) - int(1)}')</td>
  </tr>
  <tr>
    <td>print 1 * 1</td>
    <td>print(f'{int(1) * int(1)}')</td>
  </tr>
  <tr>
    <td>print 1 / 1</td>
    <td>print(f'{int(1) / int(1)}')</td>
  </tr>
  <tr>
    <td>a is 1<br/>print a</td>
    <td>a = '1'<br/>print(f'{a}')</td>
  </tr>
  <tr>
    <td>forward</td>
    <td>t = turtle.Turtle()<br>t.forward(50)</td>
  </tr>
  <tr>
    <td>forward 50</td>
    <td>t = turtle.Turtle()<br>t.forward(50)</td>
  </tr>
  <tr>
    <td>a is 50<br/>forward a</td>
    <td>a = '50'<br/>t = turtle.Turtle()<br>t.forward(a)</td>
  </tr>
  <tr>
    <td>turn</td>
    <td>t = turtle.Turtle()<br>t.right(90)</td>
  </tr>
  <tr>
    <td>turn 90</td>
    <td>t = turtle.Turtle()<br>t.right(90)</td>
  </tr>
  <tr>
    <td>a is 50<br/>turn a</td>
    <td>a = '50'<br/>t = turtle.Turtle()<br>t.right(a)</td>
  </tr>
  <tr>
    <td>sleep</td>
    <td>time.sleep(1)</td>
  </tr>
  <tr>
    <td>sleep 1</td>
    <td>time.sleep(1)</td>
  </tr>
  <tr>
    <td>x is ask 'y'<br>print x</td>
    <td>x = input('y')<br>print(x)</td>
  </tr>
  <tr>
    <td>x is a, b, c<br>print x at random</td>
    <td>x = ['a', 'b', 'c']<br>print(random.choice(x))</td>
  </tr>
  <tr>
    <td>a is 1, 2, 3<br/>f is 4<br/>add f to a</td>
    <td>a = ['1', '2', '3']<br/>f = '4'<br/>a.append(f)</td>
  </tr>
  <tr>
    <td>a is 1, 2, 3<br/>f is 4<br/>remove f from a</td>
    <td>a = ['1', '2', '3']<br/>f = '4'<br/>try:<br/>&emsp;&emsp;a.remove(f)<br/>except:<br/>&emsp;&emsp;pass</td>
  </tr>
  <tr>
    <td>a is 1, 2, 3<br/>f is 4<br/>remove f from a</td>
    <td>a = ['1', '2', '3']<br/>f = '4'<br/>try:<br/>&emsp;&emsp;a.remove(f)<br/>except:<br/>&emsp;&emsp;pass</td>
  </tr>
  <tr>
    <td>name is Hedy<br/>if name is Hedy<br/>&emsp;&emsp;print 'great'<br/>else<br/>&emsp;&emsp;print 'fine'</td>
    <td>name = 'Hedy'<br/>if name == 'Hedy':<br/>&emsp;&emsp;print(f'great')<br/>else:<br/>&emsp;&emsp;print(f'fine')</td>
  </tr>
  <tr>
    <td>items is red, green<br/>selected is red<br/>if selected in items<br/>&emsp;&emsp;print 'found!'</td>
    <td>items = ['red', 'green']<br/>selected = 'red'<br/>if selected in items:<br/>&emsp;&emsp;print(f'found!')</td>
  </tr>
  <tr>
    <td>repeat 3 times<br/>&emsp;&emsp;print 'hello!'</td>
    <td>for i in range(int('3')):<br/>&emsp;&emsp;print(f'hello!')</td>
  </tr>
  <tr>
    <td>n is 3<br/>repeat n times<br/>&emsp;&emsp;print 'hello!'</td>
    <td>n = '3'<br/>for i in range(int(n)):<br/>&emsp;&emsp;print(f'hello!')</td>
  </tr>
</tbody>
</table>


#### Incorrect Programs

<table>
<thead>
  <tr>
    <th>Hedy</th>
    <th>Exception</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td>print</td>
    <td>Incomplete Exception</td>
  </tr>
  <tr>
    <td>print'x'</td>
    <td>Invalid command</td>
  </tr>
  <tr>
    <td>print 1.0 + 1</td>
    <td>Unsupported decimal number</td>
  </tr>
  <tr>
    <td>print 1,0 + 1</td>
    <td>Unsupported decimal number</td>
  </tr>
  <tr>
    <td>ask</td>
    <td>Incomplete Exception</td>
  </tr>
    <tr>
    <td>(ask | print) (any text without quotes around it)</td>
    <td>Unquoted Text Exception</td>
  </tr>
  <tr>
    <td>(not (print | ask | forward | turn)) (any text) (not is) (any text)?</td>
    <td>Invalid Exception</td>
  </tr>
  <tr>
    <td>_SPACE (print | ask | forward | turn) (any text)?</td>
    <td>Invalid space</td>
  </tr>
  <tr>
    <td>_SPACE (any text) is (any text)?</td>
    <td>Invalid space</td>
  </tr>
  <tr>
    <td>a is 1, 2, 3<br/>answer is ask 'Is the number in ' a</td>
    <td>Invalid Argument Type Exception</td>
  </tr>  
  <tr>
    <td>(forward | turn) text</td>
    <td>Invalid Argument Type Exception</td>
  </tr>
  <tr>
    <td>a is text<br/>(forward | turn) a</td>
    <td>Invalid Argument Type Exception</td>
  </tr>
  <tr>
    <td>a is 1, 2, 3<br/>(forward | turn) a</td>
    <td>Invalid Argument Type Exception</td>
  </tr>
  <tr>
    <td>a is 1, 2, 3<br/>f is 4<br/>(add | remove) a (to | from) f</td>
    <td>Invalid Argument Type Exception</td>
  </tr>
  <tr>
    <td>items is 1, 2, 3<br/>print items</td>
    <td>Invalid Argument Type Exception</td>
  </tr>
  <tr>
    <td>a is 'test'<br/>print a + 1</td>
    <td>Invalid Argument Type Exception</td>
  </tr>
  <tr>
    <td>a is 'text'<br/>one is 1<br/>if one in a<br/>&emsp;&emsp;print 'found!'</td>
    <td>Invalid Argument Type Exception</td>
  </tr>
  <tr>
    <td>name is 1, 2<br/>if '1' is name<br/>&emsp;&emsp;print 'found'</td>
    <td>Invalid Argument Type Exception</td>
  </tr>
  <tr>
    <td>repeat 3 times print 'hello!'</td>
    <td>Invalid command (TODO: this has to be improved)</td>
  </tr>
</tbody>
</table>


## Level 9

### Commands and types

Level 9 supports:

<table>
<thead>
  <tr>
    <th>Command</th>
    <th>Types</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td>print</td>
    <td>integer | string | input</td>
  </tr>
  <tr>
    <td>ask*</td>
    <td>integer | string | input</td>
  </tr>
  <tr>
    <td>forward</td>
    <td>integer | empty | input</td>
  </tr>
  <tr>
    <td>turn</td>
    <td>integer | empty | input</td>
  </tr>
  <tr>
    <td>is</td>
    <td>string (before `is`) + any (after `is`)</td>
  </tr>
  <tr>
    <td>sleep</td>
    <td>empty | integer</td>
  </tr>
  <tr>
    <td>at random</td>
    <td>list</td>
  </tr>
  <tr>
    <td>add to</td>
    <td>list</td>
  </tr>
  <tr>
    <td>remove from</td>
    <td>list</td>
  </tr>
  <tr>
    <td>if</td>
    <td>boolean</td>
  </tr>
  <tr>
    <td>if else</td>
    <td>boolean</td>
  </tr>
  <tr>
    <td>in</td>
    <td>any (before `in`) + list (after `in`)</td>
  </tr>
  <tr>
    <td>repeat</td>
    <td>integer + 'times' | input + 'times'</td>
  </tr>
</tbody>
</table>

* \* We have to use `ask` in combination with `is`, so we get `<variablename> is ask <outputquestion>`. This way, the answer of the user will be stored in a variable.



#### Correct Programs

<table>
<thead>
  <tr>
    <th>Hedy</th>
    <th>Python</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td>print 'x' 'y'</td>
    <td>print('xy')</td>
  </tr>
  <tr>
    <td>print 1 + 1</td>
    <td>print(f'{int(1) + int(1)}')</td>
  </tr>
  <tr>
    <td>print 1 - 1</td>
    <td>print(f'{int(1) - int(1)}')</td>
  </tr>
  <tr>
    <td>print 1 * 1</td>
    <td>print(f'{int(1) * int(1)}')</td>
  </tr>
  <tr>
    <td>print 1 / 1</td>
    <td>print(f'{int(1) / int(1)}')</td>
  </tr>
  <tr>
    <td>a is 1<br/>print a</td>
    <td>a = '1'<br/>print(f'{a}')</td>
  </tr>
  <tr>
    <td>forward</td>
    <td>t = turtle.Turtle()<br>t.forward(50)</td>
  </tr>
  <tr>
    <td>forward 50</td>
    <td>t = turtle.Turtle()<br>t.forward(50)</td>
  </tr>
  <tr>
    <td>a is 50<br/>forward a</td>
    <td>a = '50'<br/>t = turtle.Turtle()<br>t.forward(a)</td>
  </tr>
  <tr>
    <td>turn</td>
    <td>t = turtle.Turtle()<br>t.right(90)</td>
  </tr>
  <tr>
    <td>turn 90</td>
    <td>t = turtle.Turtle()<br>t.right(90)</td>
  </tr>
  <tr>
    <td>a is 50<br/>turn a</td>
    <td>a = '50'<br/>t = turtle.Turtle()<br>t.right(a)</td>
  </tr>
  <tr>
    <td>sleep</td>
    <td>time.sleep(1)</td>
  </tr>
  <tr>
    <td>sleep 1</td>
    <td>time.sleep(1)</td>
  </tr>
  <tr>
    <td>x is ask 'y'<br>print x</td>
    <td>x = input('y')<br>print(x)</td>
  </tr>
  <tr>
    <td>x is a, b, c<br>print x at random</td>
    <td>x = ['a', 'b', 'c']<br>print(random.choice(x))</td>
  </tr>
  <tr>
    <td>a is 1, 2, 3<br/>f is 4<br/>add f to a</td>
    <td>a = ['1', '2', '3']<br/>f = '4'<br/>a.append(f)</td>
  </tr>
  <tr>
    <td>a is 1, 2, 3<br/>f is 4<br/>remove f from a</td>
    <td>a = ['1', '2', '3']<br/>f = '4'<br/>try:<br/>&emsp;&emsp;a.remove(f)<br/>except:<br/>&emsp;&emsp;pass</td>
  </tr>
  <tr>
    <td>a is 1, 2, 3<br/>f is 4<br/>remove f from a</td>
    <td>a = ['1', '2', '3']<br/>f = '4'<br/>try:<br/>&emsp;&emsp;a.remove(f)<br/>except:<br/>&emsp;&emsp;pass</td>
  </tr>
  <tr>
    <td>name is Hedy<br/>if name is Hedy<br/>&emsp;&emsp;print 'great'<br/>else<br/>&emsp;&emsp;print 'fine'</td>
    <td>name = 'Hedy'<br/>if name == 'Hedy':<br/>&emsp;&emsp;print(f'great')<br/>else:<br/>&emsp;&emsp;print(f'fine')</td>
  </tr>
  <tr>
    <td>items is red, green<br/>selected is red<br/>if selected in items<br/>&emsp;&emsp;print 'found!'</td>
    <td>items = ['red', 'green']<br/>selected = 'red'<br/>if selected in items:<br/>&emsp;&emsp;print(f'found!')</td>
  </tr>
  <tr>
    <td>repeat 3 times<br/>&emsp;&emsp;print 'hello!'</td>
    <td>for i in range(int('3')):<br/>&emsp;&emsp;print(f'hello!')</td>
  </tr>
  <tr>
    <td>n is 3<br/>repeat n times<br/>&emsp;&emsp;print 'hello!'</td>
    <td>n = '3'<br/>for i in range(int(n)):<br/>&emsp;&emsp;print(f'hello!')</td>
  </tr>
</tbody>
</table>


#### Incorrect Programs

<table>
<thead>
  <tr>
    <th>Hedy</th>
    <th>Exception</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td>print</td>
    <td>Incomplete Exception</td>
  </tr>
  <tr>
    <td>print'x'</td>
    <td>Invalid command</td>
  </tr>
  <tr>
    <td>print 1.0 + 1</td>
    <td>Unsupported decimal number</td>
  </tr>
  <tr>
    <td>print 1,0 + 1</td>
    <td>Unsupported decimal number</td>
  </tr>
  <tr>
    <td>ask</td>
    <td>Incomplete Exception</td>
  </tr>
    <tr>
    <td>(ask | print) (any text without quotes around it)</td>
    <td>Unquoted Text Exception</td>
  </tr>
  <tr>
    <td>(not (print | ask | forward | turn)) (any text) (not is) (any text)?</td>
    <td>Invalid Exception</td>
  </tr>
  <tr>
    <td>_SPACE (print | ask | forward | turn) (any text)?</td>
    <td>Invalid space</td>
  </tr>
  <tr>
    <td>_SPACE (any text) is (any text)?</td>
    <td>Invalid space</td>
  </tr>
  <tr>
    <td>a is 1, 2, 3<br/>answer is ask 'Is the number in ' a</td>
    <td>Invalid Argument Type Exception</td>
  </tr>  
  <tr>
    <td>(forward | turn) text</td>
    <td>Invalid Argument Type Exception</td>
  </tr>
  <tr>
    <td>a is text<br/>(forward | turn) a</td>
    <td>Invalid Argument Type Exception</td>
  </tr>
  <tr>
    <td>a is 1, 2, 3<br/>(forward | turn) a</td>
    <td>Invalid Argument Type Exception</td>
  </tr>
  <tr>
    <td>a is 1, 2, 3<br/>f is 4<br/>(add | remove) a (to | from) f</td>
    <td>Invalid Argument Type Exception</td>
  </tr>
  <tr>
    <td>items is 1, 2, 3<br/>print items</td>
    <td>Invalid Argument Type Exception</td>
  </tr>
  <tr>
    <td>a is 'test'<br/>print a + 1</td>
    <td>Invalid Argument Type Exception</td>
  </tr>
  <tr>
    <td>a is 'text'<br/>one is 1<br/>if one in a<br/>&emsp;&emsp;print 'found!'</td>
    <td>Invalid Argument Type Exception</td>
  </tr>
  <tr>
    <td>name is 1, 2<br/>if '1' is name<br/>&emsp;&emsp;print 'found'</td>
    <td>Invalid Argument Type Exception</td>
  </tr>
  <tr>
    <td>repeat 3 times print 'hello!'</td>
    <td>Invalid command (TODO: this has to be improved)</td>
  </tr>
</tbody>
</table>

## Level 10

### Commands and types

Level 10 supports:

<table>
<thead>
  <tr>
    <th>Command</th>
    <th>Types</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td>print</td>
    <td>integer | string | input</td>
  </tr>
  <tr>
    <td>ask*</td>
    <td>integer | string | input</td>
  </tr>
  <tr>
    <td>forward</td>
    <td>integer | empty | input</td>
  </tr>
  <tr>
    <td>turn</td>
    <td>integer | empty | input</td>
  </tr>
  <tr>
    <td>is</td>
    <td>string (before `is`) + any (after `is`)</td>
  </tr>
  <tr>
    <td>sleep</td>
    <td>empty | integer</td>
  </tr>
  <tr>
    <td>at random</td>
    <td>list</td>
  </tr>
  <tr>
    <td>add to</td>
    <td>list</td>
  </tr>
  <tr>
    <td>remove from</td>
    <td>list</td>
  </tr>
  <tr>
    <td>if</td>
    <td>boolean</td>
  </tr>
  <tr>
    <td>if else</td>
    <td>boolean</td>
  </tr>
  <tr>
    <td>in</td>
    <td>any (before `in`) + list (after `in`)</td>
  </tr>
  <tr>
    <td>repeat</td>
    <td>integer + 'times' | input + 'times'</td>
  </tr>
  <tr>
    <td>for</td>
    <td>string + 'in' + list</td>
  </tr>
</tbody>
</table>

* \* We have to use `ask` in combination with `is`, so we get `<variablename> is ask <outputquestion>`. This way, the answer of the user will be stored in a variable.


#### Correct Programs

<table>
<thead>
  <tr>
    <th>Hedy</th>
    <th>Python</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td>print 'x' 'y'</td>
    <td>print('xy')</td>
  </tr>
  <tr>
    <td>print 1 + 1</td>
    <td>print(f'{int(1) + int(1)}')</td>
  </tr>
  <tr>
    <td>print 1 - 1</td>
    <td>print(f'{int(1) - int(1)}')</td>
  </tr>
  <tr>
    <td>print 1 * 1</td>
    <td>print(f'{int(1) * int(1)}')</td>
  </tr>
  <tr>
    <td>print 1 / 1</td>
    <td>print(f'{int(1) / int(1)}')</td>
  </tr>
  <tr>
    <td>a is 1<br/>print a</td>
    <td>a = '1'<br/>print(f'{a}')</td>
  </tr>
  <tr>
    <td>forward</td>
    <td>t = turtle.Turtle()<br>t.forward(50)</td>
  </tr>
  <tr>
    <td>forward 50</td>
    <td>t = turtle.Turtle()<br>t.forward(50)</td>
  </tr>
  <tr>
    <td>a is 50<br/>forward a</td>
    <td>a = '50'<br/>t = turtle.Turtle()<br>t.forward(a)</td>
  </tr>
  <tr>
    <td>turn</td>
    <td>t = turtle.Turtle()<br>t.right(90)</td>
  </tr>
  <tr>
    <td>turn 90</td>
    <td>t = turtle.Turtle()<br>t.right(90)</td>
  </tr>
  <tr>
    <td>a is 50<br/>turn a</td>
    <td>a = '50'<br/>t = turtle.Turtle()<br>t.right(a)</td>
  </tr>
  <tr>
    <td>sleep</td>
    <td>time.sleep(1)</td>
  </tr>
  <tr>
    <td>sleep 1</td>
    <td>time.sleep(1)</td>
  </tr>
  <tr>
    <td>x is ask 'y'<br>print x</td>
    <td>x = input('y')<br>print(x)</td>
  </tr>
  <tr>
    <td>x is a, b, c<br>print x at random</td>
    <td>x = ['a', 'b', 'c']<br>print(random.choice(x))</td>
  </tr>
  <tr>
    <td>a is 1, 2, 3<br/>f is 4<br/>add f to a</td>
    <td>a = ['1', '2', '3']<br/>f = '4'<br/>a.append(f)</td>
  </tr>
  <tr>
    <td>a is 1, 2, 3<br/>f is 4<br/>remove f from a</td>
    <td>a = ['1', '2', '3']<br/>f = '4'<br/>try:<br/>&emsp;&emsp;a.remove(f)<br/>except:<br/>&emsp;&emsp;pass</td>
  </tr>
  <tr>
    <td>a is 1, 2, 3<br/>f is 4<br/>remove f from a</td>
    <td>a = ['1', '2', '3']<br/>f = '4'<br/>try:<br/>&emsp;&emsp;a.remove(f)<br/>except:<br/>&emsp;&emsp;pass</td>
  </tr>
  <tr>
    <td>name is Hedy<br/>if name is Hedy<br/>&emsp;&emsp;print 'great'<br/>else<br/>&emsp;&emsp;print 'fine'</td>
    <td>name = 'Hedy'<br/>if name == 'Hedy':<br/>&emsp;&emsp;print(f'great')<br/>else:<br/>&emsp;&emsp;print(f'fine')</td>
  </tr>
  <tr>
    <td>items is red, green<br/>selected is red<br/>if selected in items<br/>&emsp;&emsp;print 'found!'</td>
    <td>items = ['red', 'green']<br/>selected = 'red'<br/>if selected in items:<br/>&emsp;&emsp;print(f'found!')</td>
  </tr>
  <tr>
    <td>repeat 3 times<br/>&emsp;&emsp;print 'hello!'</td>
    <td>for i in range(int('3')):<br/>&emsp;&emsp;print(f'hello!')</td>
  </tr>
  <tr>
    <td>n is 3<br/>repeat n times<br/>&emsp;&emsp;print 'hello!'</td>
    <td>n = '3'<br/>for i in range(int(n)):<br/>&emsp;&emsp;print(f'hello!')</td>
  </tr>
  <tr>
    <td>ns is 1, 2, 3<br/>for n in ns<br/>&emsp;&emsp;print n</td>
    <td>ns = ['1', '2', '3']<br/>for n in ns:<br/>&emsp;&emsp;print(f'{n}')</td> 
</tr>
</tbody>
</table>


#### Incorrect Programs

<table>
<thead>
  <tr>
    <th>Hedy</th>
    <th>Exception</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td>print</td>
    <td>Incomplete Exception</td>
  </tr>
  <tr>
    <td>print'x'</td>
    <td>Invalid command</td>
  </tr>
  <tr>
    <td>print 1.0 + 1</td>
    <td>Unsupported decimal number</td>
  </tr>
  <tr>
    <td>print 1,0 + 1</td>
    <td>Unsupported decimal number</td>
  </tr>
  <tr>
    <td>ask</td>
    <td>Incomplete Exception</td>
  </tr>
    <tr>
    <td>(ask | print) (any text without quotes around it)</td>
    <td>Unquoted Text Exception</td>
  </tr>
  <tr>
    <td>(not (print | ask | forward | turn)) (any text) (not is) (any text)?</td>
    <td>Invalid Exception</td>
  </tr>
  <tr>
    <td>_SPACE (print | ask | forward | turn) (any text)?</td>
    <td>Invalid space</td>
  </tr>
  <tr>
    <td>_SPACE (any text) is (any text)?</td>
    <td>Invalid space</td>
  </tr>
  <tr>
    <td>a is 1, 2, 3<br/>answer is ask 'Is the number in ' a</td>
    <td>Invalid Argument Type Exception</td>
  </tr>  
  <tr>
    <td>(forward | turn) text</td>
    <td>Invalid Argument Type Exception</td>
  </tr>
  <tr>
    <td>a is text<br/>(forward | turn) a</td>
    <td>Invalid Argument Type Exception</td>
  </tr>
  <tr>
    <td>a is 1, 2, 3<br/>(forward | turn) a</td>
    <td>Invalid Argument Type Exception</td>
  </tr>
  <tr>
    <td>a is 1, 2, 3<br/>f is 4<br/>(add | remove) a (to | from) f</td>
    <td>Invalid Argument Type Exception</td>
  </tr>
  <tr>
    <td>items is 1, 2, 3<br/>print items</td>
    <td>Invalid Argument Type Exception</td>
  </tr>
  <tr>
    <td>a is 'test'<br/>print a + 1</td>
    <td>Invalid Argument Type Exception</td>
  </tr>
  <tr>
    <td>a is 'text'<br/>one is 1<br/>if one in a<br/>&emsp;&emsp;print 'found!'</td>
    <td>Invalid Argument Type Exception</td>
  </tr>
  <tr>
    <td>name is 1, 2<br/>if '1' is name<br/>&emsp;&emsp;print 'found'</td>
    <td>Invalid Argument Type Exception</td>
  </tr>
  <tr>
    <td>repeat 3 times print 'hello!'</td>
    <td>Invalid command (TODO: this has to be improved)</td>
  </tr>
</tbody>
</table>


## Level 11

### Commands and types

Level 11 supports:

<table>
<thead>
  <tr>
    <th>Command</th>
    <th>Types</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td>print</td>
    <td>integer | string | input</td>
  </tr>
  <tr>
    <td>ask*</td>
    <td>integer | string | input</td>
  </tr>
  <tr>
    <td>is</td>
    <td>string (before `is`) + any (after `is`)</td>
  </tr>
  <tr>
    <td>sleep</td>
    <td>empty | integer</td>
  </tr>
  <tr>
    <td>at random</td>
    <td>list</td>
  </tr>
  <tr>
    <td>add to</td>
    <td>list</td>
  </tr>
  <tr>
    <td>remove from</td>
    <td>list</td>
  </tr>
  <tr>
    <td>if</td>
    <td>boolean</td>
  </tr>
  <tr>
    <td>if else</td>
    <td>boolean</td>
  </tr>
  <tr>
    <td>in</td>
    <td>any (before `in`) + list (after `in`)</td>
  </tr>
  <tr>
    <td>for</td>
    <td>string + 'in' + list | string + 'in' + 'range' + (integer | input) + 'to' + (integer | input) </td>
  </tr>
</tbody>
</table>

* \* We have to use `ask` in combination with `is`, so we get `<variablename> is ask <outputquestion>`. This way, the answer of the user will be stored in a variable.


#### Correct Programs

<table>
<thead>
  <tr>
    <th>Hedy</th>
    <th>Python</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td>print 'x' 'y'</td>
    <td>print('xy')</td>
  </tr>
  <tr>
    <td>print 1 + 1</td>
    <td>print(f'{int(1) + int(1)}')</td>
  </tr>
  <tr>
    <td>print 1 - 1</td>
    <td>print(f'{int(1) - int(1)}')</td>
  </tr>
  <tr>
    <td>print 1 * 1</td>
    <td>print(f'{int(1) * int(1)}')</td>
  </tr>
  <tr>
    <td>print 1 / 1</td>
    <td>print(f'{int(1) / int(1)}')</td>
  </tr>
  <tr>
    <td>a is 1<br/>print a</td>
    <td>a = '1'<br/>print(f'{a}')</td>
  </tr>
  <tr>
    <td>sleep</td>
    <td>time.sleep(1)</td>
  </tr>
  <tr>
    <td>sleep 1</td>
    <td>time.sleep(1)</td>
  </tr>
  <tr>
    <td>x is ask 'y'<br>print x</td>
    <td>x = input('y')<br>print(x)</td>
  </tr>
  <tr>
    <td>x is a, b, c<br>print x at random</td>
    <td>x = ['a', 'b', 'c']<br>print(random.choice(x))</td>
  </tr>
  <tr>
    <td>a is 1, 2, 3<br/>f is 4<br/>add f to a</td>
    <td>a = ['1', '2', '3']<br/>f = '4'<br/>a.append(f)</td>
  </tr>
  <tr>
    <td>a is 1, 2, 3<br/>f is 4<br/>remove f from a</td>
    <td>a = ['1', '2', '3']<br/>f = '4'<br/>try:<br/>&emsp;&emsp;a.remove(f)<br/>except:<br/>&emsp;&emsp;pass</td>
  </tr>
  <tr>
    <td>a is 1, 2, 3<br/>f is 4<br/>remove f from a</td>
    <td>a = ['1', '2', '3']<br/>f = '4'<br/>try:<br/>&emsp;&emsp;a.remove(f)<br/>except:<br/>&emsp;&emsp;pass</td>
  </tr>
  <tr>
    <td>name is Hedy<br/>if name is Hedy<br/>&emsp;&emsp;print 'great'<br/>else<br/>&emsp;&emsp;print 'fine'</td>
    <td>name = 'Hedy'<br/>if name == 'Hedy':<br/>&emsp;&emsp;print(f'great')<br/>else:<br/>&emsp;&emsp;print(f'fine')</td>
  </tr>
  <tr>
    <td>items is red, green<br/>selected is red<br/>if selected in items<br/>&emsp;&emsp;print 'found!'</td>
    <td>items = ['red', 'green']<br/>selected = 'red'<br/>if selected in items:<br/>&emsp;&emsp;print(f'found!')</td>
  </tr>
  <tr>
    <td>ns is 1, 2, 3<br/>for n in ns<br/>&emsp;&emsp;print n</td>
    <td>ns = ['1', '2', '3']<br/>for n in ns:<br/>&emsp;&emsp;print(f'{n}')</td> 
  </tr>
  <tr>
    <td>for a in range 2 to 4<br/>&emsp;&emsp;a is a + 2</td>
    <td>step = 1 if int(2) < int(4) else -1<br/>for a in range(int(2), int(4) + step, step):<br/>&emsp;&emsp;a = int(a) + int(2)</td>
</tr>
</tbody>
</table>


#### Incorrect Programs

<table>
<thead>
  <tr>
    <th>Hedy</th>
    <th>Exception</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td>print</td>
    <td>Incomplete Exception</td>
  </tr>
  <tr>
    <td>print'x'</td>
    <td>Invalid command</td>
  </tr>
  <tr>
    <td>print 1.0 + 1</td>
    <td>Unsupported decimal number</td>
  </tr>
  <tr>
    <td>print 1,0 + 1</td>
    <td>Unsupported decimal number</td>
  </tr>
  <tr>
    <td>ask</td>
    <td>Incomplete Exception</td>
  </tr>
    <tr>
    <td>(ask | print) (any text without quotes around it)</td>
    <td>Unquoted Text Exception</td>
  </tr>
  <tr>
    <td>(not (print | ask)) (any text) (not is) (any text)?</td>
    <td>Invalid Exception</td>
  </tr>
  <tr>
    <td>_SPACE (print | ask) (any text)?</td>
    <td>Invalid space</td>
  </tr>
  <tr>
    <td>_SPACE (any text) is (any text)?</td>
    <td>Invalid space</td>
  </tr>
  <tr>
    <td>a is 1, 2, 3<br/>answer is ask 'Is the number in ' a</td>
    <td>Invalid Argument Type Exception</td>
  </tr>
  <tr>
    <td>a is 1, 2, 3<br/>f is 4<br/>(add | remove) a (to | from) f</td>
    <td>Invalid Argument Type Exception</td>
  </tr>
  <tr>
    <td>items is 1, 2, 3<br/>print items</td>
    <td>Invalid Argument Type Exception</td>
  </tr>
  <tr>
    <td>a is 'test'<br/>print a + 1</td>
    <td>Invalid Argument Type Exception</td>
  </tr>
  <tr>
    <td>a is 'text'<br/>one is 1<br/>if one in a<br/>&emsp;&emsp;print 'found!'</td>
    <td>Invalid Argument Type Exception</td>
  </tr>
  <tr>
    <td>name is 1, 2<br/>if '1' is name<br/>&emsp;&emsp;print 'found'</td>
    <td>Invalid Argument Type Exception</td>
  </tr>
  <tr>
    <td>for a in range 1 to 10<br/>print 'hello!'</td>
    <td>No Indentation Exception</td>
  </tr>
</tbody>
</table>

## Level 12

### Commands and types

Level 12 supports:

<table>
<thead>
  <tr>
    <th>Command</th>
    <th>Types</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td>print</td>
    <td>integer | string | float | input</td>
  </tr>
  <tr>
    <td>ask*</td>
    <td>integer | string | float | input</td>
  </tr>
  <tr>
    <td>is | =</td>
    <td>string (before `is`) + any (after `is`)</td>
  </tr>
  <tr>
    <td>sleep</td>
    <td>empty | integer</td>
  </tr>
  <tr>
    <td>at random</td>
    <td>list</td>
  </tr>
  <tr>
    <td>add to</td>
    <td>list</td>
  </tr>
  <tr>
    <td>remove from</td>
    <td>list</td>
  </tr>
  <tr>
    <td>if</td>
    <td>boolean</td>
  </tr>
  <tr>
    <td>if else</td>
    <td>boolean</td>
  </tr>
  <tr>
    <td>in</td>
    <td>any (before `in`) + list (after `in`)</td>
  </tr>
  <tr>
    <td>for</td>
    <td>string + 'in' + list | string + 'in' + 'range' + (integer | input) + 'to' + (integer | input)</td>
  </tr>
</tbody>
</table>

* \* We have to use `ask` in combination with `is`, so we get `<variablename> is ask <outputquestion>`. This way, the answer of the user will be stored in a variable.


#### Correct Programs

<table>
<thead>
  <tr>
    <th>Hedy</th>
    <th>Python</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td>print 'x' 'y'</td>
    <td>print('xy')</td>
  </tr>
  <tr>
    <td>print 1 + 1</td>
    <td>print(f'{1 + 1}')</td>
  </tr>
  <tr>
    <td>print 1 - 1</td>
    <td>print(f'{1 - 1}')</td>
  </tr>
  <tr>
    <td>print 1 * 1</td>
    <td>print(f'{1 * 1}')</td>
  </tr>
  <tr>
    <td>print 1 / 1</td>
    <td>print(f'{1 / 1}')</td>
  </tr>
   <tr>
    <td>print 1.0 + 1</td>
    <td>print(f'{1.0 / 1}')</td>
  </tr>
  <tr>
    <td>a is 1<br/>print a</td>
    <td>a = 1<br/>print(f'{a}')</td>
  </tr>
  <tr>
    <td>a is 1.0<br/>print a</td>
    <td>a = 1.0<br/>print(f'{a}')</td>
  </tr>
  <tr>
    <td>a is 'text'<br/>print a</td>
    <td>a = 'text'<br/>print(f'{a}')</td>
  </tr>
  <tr>
    <td>sleep</td>
    <td>time.sleep(1)</td>
  </tr>
  <tr>
    <td>sleep 1</td>
    <td>time.sleep(1)</td>
  </tr>
  <tr>
    <td>x is ask 'y'<br>print x</td>
    <td>x = input('y')<br>try:<br>&emsp;&emsp;x = int(x)<br>except ValueError:<br/>&emsp;&emsp;x = float(x)<br>&emsp;&emsp;except ValueError:<br/>&emsp;&emsp;&emsp;&emsp;pass<br/>print(x)</td>
  </tr>
  <tr>
    <td>x is 'a', 'b', 'c'<br>print x at random</td>
    <td>x = ['a', 'b', 'c']<br>print(random.choice(x))</td>
  </tr>
  <tr>
    <td>a is 1, 2, 3<br/>f is 4<br/>add f to a</td>
    <td>a = [1, 2, 3]<br/>f = 4<br/>a.append(f)</td>
  </tr>
  <tr>
    <td>a is 1, 2, 3<br/>f is 4<br/>remove f from a</td>
    <td>a = [1, 2, 3]<br/>f = 4<br/>try:<br/>&emsp;&emsp;a.remove(f)<br/>except:<br/>&emsp;&emsp;pass</td>
  </tr>
  <tr>
    <td>a is 1, 2, 3<br/>f is 4<br/>remove f from a</td>
    <td>a = [1, 2, 3]<br/>f = 4<br/>try:<br/>&emsp;&emsp;a.remove(f)<br/>except:<br/>&emsp;&emsp;pass</td>
  </tr>
  <tr>
    <td>name is 'Hedy'<br/>if name is 'Hedy'<br/>&emsp;&emsp;print 'great'<br/>else<br/>&emsp;&emsp;print 'fine'</td>
    <td>name = 'Hedy'<br/>if name == 'Hedy':<br/>&emsp;&emsp;print(f'great')<br/>else:<br/>&emsp;&emsp;print(f'fine')</td>
  </tr>
  <tr>
    <td>items is 'red', 'green'<br/>selected is 'red'<br/>if selected in items<br/>&emsp;&emsp;print 'found!'</td>
    <td>items = ['red', 'green']<br/>selected = 'red'<br/>if selected in items:<br/>&emsp;&emsp;print(f'found!')</td>
  </tr>
  <tr>
    <td>ns is 1, 2, 3<br/>for n in ns<br/>&emsp;&emsp;print n</td>
    <td>ns = [1, 2, 3]<br/>for n in ns:<br/>&emsp;&emsp;print(f'{n}')</td> 
  </tr>
  <tr>
    <td>for a in range 2 to 4<br/>&emsp;&emsp;a is a + 2</td>
    <td>step = 1 if int(2) < int(4) else -1<br/>for a in range(int(2), int(4) + step, step):<br/>&emsp;&emsp;a = a + 2</td>
</tr>
</tbody>
</table>


#### Incorrect Programs

<table>
<thead>
  <tr>
    <th>Hedy</th>
    <th>Exception</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td>print</td>
    <td>Incomplete Exception</td>
  </tr>
  <tr>
    <td>print'x'</td>
    <td>Invalid command</td>
  </tr>
  <tr>
    <td>print 1,0 + 1</td>
    <td>Invalid Command (TODO: this could be improved)</td>
  </tr>
  <tr>
    <td>ask</td>
    <td>Incomplete Exception</td>
  </tr>
    <tr>
    <td>(ask | print) (any text without quotes around it)</td>
    <td>Unquoted Text Exception</td>
  </tr>
  <tr>
    <td>(not (print | ask)) (any text) (not is) (any text)?</td>
    <td>Invalid Exception</td>
  </tr>
  <tr>
    <td>_SPACE (print | ask) (any text)?</td>
    <td>Invalid space</td>
  </tr>
  <tr>
    <td>_SPACE (any text) is (any text)?</td>
    <td>Invalid space</td>
  </tr>
  <tr>
    <td>a is 1, 2, 3<br/>answer is ask 'Is the number in ' a</td>
    <td>Invalid Argument Type Exception</td>
  </tr>
  <tr>
    <td>a is 1, 2, 3<br/>f is 4<br/>(add | remove) a (to | from) f</td>
    <td>Invalid Argument Type Exception</td>
  </tr>
  <tr>
    <td>items is 1, 2, 3<br/>print items</td>
    <td>Invalid Argument Type Exception</td>
  </tr>
  <tr>
    <td>a is 'test'<br/>print a + 1</td>
    <td>Invalid Argument Type Exception</td>
  </tr>
  <tr>
    <td>a is 'text'<br/>one is 1<br/>if one in a<br/>&emsp;&emsp;print 'found!'</td>
    <td>Invalid Argument Type Exception</td>
  </tr>
  <tr>
    <td>name is 1, 2<br/>if '1' is name<br/>&emsp;&emsp;print 'found'</td>
    <td>Invalid Argument Type Exception</td>
  </tr>
  <tr>
    <td>for a in range 1 to 10<br/>print 'hello!'</td>
    <td>No Indentation Exception</td>
  </tr>
</tbody>
</table>


## Level 13

### Commands and types

Level 13 supports:

<table>
<thead>
  <tr>
    <th>Command</th>
    <th>Types</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td>print</td>
    <td>integer | string | float | input</td>
  </tr>
  <tr>
    <td>ask*</td>
    <td>integer | string | float | input</td>
  </tr>
  <tr>
    <td>is | =</td>
    <td>string (before `is`) + any (after `is`)</td>
  </tr>
  <tr>
    <td>sleep</td>
    <td>empty | integer</td>
  </tr>
  <tr>
    <td>at random</td>
    <td>list</td>
  </tr>
  <tr>
    <td>add to</td>
    <td>list</td>
  </tr>
  <tr>
    <td>remove from</td>
    <td>list</td>
  </tr>
  <tr>
    <td>if</td>
    <td>boolean</td>
  </tr>
  <tr>
    <td>if else</td>
    <td>boolean</td>
  </tr>
  <tr>
    <td>in</td>
    <td>any (before `in`) + list (after `in`)</td>
  </tr>
  <tr>
    <td>for</td>
    <td>string + 'in' + list | string + 'in' + 'range' + (integer | input) + 'to' + (integer | input)</td>
  </tr>
  <tr>
    <td>and</td>
    <td>boolean (on both sides of `and`)</td>
  </tr>
  <tr>
    <td>or</td>
    <td>boolean (on both sides of `or`)</td>
  </tr>
</tbody>
</table>

* \* We have to use `ask` in combination with `is`, so we get `<variablename> is ask <outputquestion>`. This way, the answer of the user will be stored in a variable.


#### Correct Programs

<table>
<thead>
  <tr>
    <th>Hedy</th>
    <th>Python</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td>print 'x' 'y'</td>
    <td>print('xy')</td>
  </tr>
  <tr>
    <td>print 1 + 1</td>
    <td>print(f'{1 + 1}')</td>
  </tr>
  <tr>
    <td>print 1 - 1</td>
    <td>print(f'{1 - 1}')</td>
  </tr>
  <tr>
    <td>print 1 * 1</td>
    <td>print(f'{1 * 1}')</td>
  </tr>
  <tr>
    <td>print 1 / 1</td>
    <td>print(f'{1 / 1}')</td>
  </tr>
   <tr>
    <td>print 1.0 + 1</td>
    <td>print(f'{1.0 / 1}')</td>
  </tr>
  <tr>
    <td>a is 1<br/>print a</td>
    <td>a = 1<br/>print(f'{a}')</td>
  </tr>
  <tr>
    <td>a is 1.0<br/>print a</td>
    <td>a = 1.0<br/>print(f'{a}')</td>
  </tr>
  <tr>
    <td>a is 'text'<br/>print a</td>
    <td>a = 'text'<br/>print(f'{a}')</td>
  </tr>
  <tr>
    <td>sleep</td>
    <td>time.sleep(1)</td>
  </tr>
  <tr>
    <td>sleep 1</td>
    <td>time.sleep(1)</td>
  </tr>
  <tr>
    <td>x is ask 'y'<br>print x</td>
    <td>x = input('y')<br>try:<br>&emsp;&emsp;x = int(x)<br>except ValueError:<br/>&emsp;&emsp;x = float(x)<br>&emsp;&emsp;except ValueError:<br/>&emsp;&emsp;&emsp;&emsp;pass<br/>print(x)</td>
  </tr>
  <tr>
    <td>x is 'a', 'b', 'c'<br>print x at random</td>
    <td>x = ['a', 'b', 'c']<br>print(random.choice(x))</td>
  </tr>
  <tr>
    <td>a is 1, 2, 3<br/>f is 4<br/>add f to a</td>
    <td>a = [1, 2, 3]<br/>f = 4<br/>a.append(f)</td>
  </tr>
  <tr>
    <td>a is 1, 2, 3<br/>f is 4<br/>remove f from a</td>
    <td>a = [1, 2, 3]<br/>f = 4<br/>try:<br/>&emsp;&emsp;a.remove(f)<br/>except:<br/>&emsp;&emsp;pass</td>
  </tr>
  <tr>
    <td>a is 1, 2, 3<br/>f is 4<br/>remove f from a</td>
    <td>a = [1, 2, 3]<br/>f = 4<br/>try:<br/>&emsp;&emsp;a.remove(f)<br/>except:<br/>&emsp;&emsp;pass</td>
  </tr>
  <tr>
    <td>name is 'Hedy'<br/>if name is 'Hedy'<br/>&emsp;&emsp;print 'great'<br/>else<br/>&emsp;&emsp;print 'fine'</td>
    <td>name = 'Hedy'<br/>if name == 'Hedy':<br/>&emsp;&emsp;print(f'great')<br/>else:<br/>&emsp;&emsp;print(f'fine')</td>
  </tr>
  <tr>
    <td>name is 'Hedy'<br/>if name is 'hedy' (or | and) name is 'Hedy'<br/>&emsp;&emsp;print 'great'<br/>else<br/>&emsp;&emsp;print 'fine'</td>
    <td>name = 'Hedy'<br/>if str(name) == str('Hedy') (or | and) str(name) == str('hedy'):<br/>&emsp;&emsp;print(f'great')<br/>else:<br/>&emsp;&emsp;print(f'fine')</td>
  </tr>
  <tr>
    <td>items is 'red', 'green'<br/>selected is 'red'<br/>if selected in items<br/>&emsp;&emsp;print 'found!'</td>
    <td>items = ['red', 'green']<br/>selected = 'red'<br/>if selected in items:<br/>&emsp;&emsp;print(f'found!')</td>
  </tr>
  <tr>
    <td>ns is 1, 2, 3<br/>for n in ns<br/>&emsp;&emsp;print n</td>
    <td>ns = [1, 2, 3]<br/>for n in ns:<br/>&emsp;&emsp;print(f'{n}')</td> 
  </tr>
  <tr>
    <td>for a in range 2 to 4<br/>&emsp;&emsp;a is a + 2</td>
    <td>step = 1 if int(2) < int(4) else -1<br/>for a in range(int(2), int(4) + step, step):<br/>&emsp;&emsp;a = a + 2</td>
</tr>
</tbody>
</table>


#### Incorrect Programs

<table>
<thead>
  <tr>
    <th>Hedy</th>
    <th>Exception</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td>print</td>
    <td>Incomplete Exception</td>
  </tr>
  <tr>
    <td>print'x'</td>
    <td>Invalid command</td>
  </tr>
  <tr>
    <td>print 1,0 + 1</td>
    <td>Invalid Command (TODO: this could be improved)</td>
  </tr>
  <tr>
    <td>ask</td>
    <td>Incomplete Exception</td>
  </tr>
    <tr>
    <td>(ask | print) (any text without quotes around it)</td>
    <td>Unquoted Text Exception</td>
  </tr>
  <tr>
    <td>(not (print | ask)) (any text) (not is) (any text)?</td>
    <td>Invalid Exception</td>
  </tr>
  <tr>
    <td>_SPACE (print | ask) (any text)?</td>
    <td>Invalid space</td>
  </tr>
  <tr>
    <td>_SPACE (any text) is (any text)?</td>
    <td>Invalid space</td>
  </tr>
  <tr>
    <td>a is 1, 2, 3<br/>answer is ask 'Is the number in ' a</td>
    <td>Invalid Argument Type Exception</td>
  </tr>
  <tr>
    <td>a is 1, 2, 3<br/>f is 4<br/>(add | remove) a (to | from) f</td>
    <td>Invalid Argument Type Exception</td>
  </tr>
  <tr>
    <td>items is 1, 2, 3<br/>print items</td>
    <td>Invalid Argument Type Exception</td>
  </tr>
  <tr>
    <td>a is 'test'<br/>print a + 1</td>
    <td>Invalid Argument Type Exception</td>
  </tr>
  <tr>
    <td>a is 'text'<br/>one is 1<br/>if one in a<br/>&emsp;&emsp;print 'found!'</td>
    <td>Invalid Argument Type Exception</td>
  </tr>
  <tr>
    <td>name is 1, 2<br/>if '1' is name<br/>&emsp;&emsp;print 'found'</td>
    <td>Invalid Argument Type Exception</td>
  </tr>
  <tr>
    <td>for a in range 1 to 10<br/>print 'hello!'</td>
    <td>No Indentation Exception</td>
  </tr>
</tbody>
</table>


## Level 14

### Commands and types

Level 14 supports:

<table>
<thead>
  <tr>
    <th>Command</th>
    <th>Types</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td>print</td>
    <td>integer | string | float | input</td>
  </tr>
  <tr>
    <td>ask*</td>
    <td>integer | string | float | input</td>
  </tr>
  <tr>
    <td>is | = (assignment)</td>
    <td>string (before `is`) + any (after `is`)</td>
  </tr>
  <tr>
    <td>sleep</td>
    <td>empty | integer</td>
  </tr>
  <tr>
    <td>at random</td>
    <td>list</td>
  </tr>
  <tr>
    <td>add to</td>
    <td>list</td>
  </tr>
  <tr>
    <td>remove from</td>
    <td>list</td>
  </tr>
  <tr>
    <td>if</td>
    <td>boolean</td>
  </tr>
  <tr>
    <td>if else</td>
    <td>boolean</td>
  </tr>
  <tr>
    <td>in</td>
    <td>any (before `in`) + list (after `in`)</td>
  </tr>
  <tr>
    <td>for</td>
    <td>string + 'in' + list | string + 'in' + 'range' + (integer | input) + 'to' + (integer | input)</td>
  </tr>
  <tr>
    <td>and</td>
    <td>boolean (on both sides of `and`)</td>
  </tr>
  <tr>
    <td>or</td>
    <td>boolean (on both sides of `or`)</td>
  </tr>
  <tr>
    <td>< **</td>
    <td>integer | float | input</td>
  </tr>
  <tr>
    <td>> **</td>
    <td>integer | float | input</td>
  </tr>
  <tr>
    <td>== | is | = (comparison)**</td>
    <td>string | integer | float | list | input</td>
  </tr>
  <tr>
    <td>!= **</td>
    <td>string | integer | float | list | input</td>
  </tr>
  <tr>
    <td><= **</td>
    <td>integer | float | input</td>
  </tr>
  <tr>
    <td>>= **</td>
    <td>integer | float | input</td>
  </tr>
</tbody>
</table>

* \* We have to use `ask` in combination with `is`, so we get `<variablename> is ask <outputquestion>`. This way, the answer of the user will be stored in a variable.

* \*\* All comparisons need to have the same type on both sides of the command. (Except when the input type is used.)

#### Correct Programs

<table>
<thead>
  <tr>
    <th>Hedy</th>
    <th>Python</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td>print 'x' 'y'</td>
    <td>print('xy')</td>
  </tr>
  <tr>
    <td>print 1 + 1</td>
    <td>print(f'{1 + 1}')</td>
  </tr>
  <tr>
    <td>print 1 - 1</td>
    <td>print(f'{1 - 1}')</td>
  </tr>
  <tr>
    <td>print 1 * 1</td>
    <td>print(f'{1 * 1}')</td>
  </tr>
  <tr>
    <td>print 1 / 1</td>
    <td>print(f'{1 / 1}')</td>
  </tr>
   <tr>
    <td>print 1.0 + 1</td>
    <td>print(f'{1.0 / 1}')</td>
  </tr>
  <tr>
    <td>a is 1<br/>print a</td>
    <td>a = 1<br/>print(f'{a}')</td>
  </tr>
  <tr>
    <td>a is 1.0<br/>print a</td>
    <td>a = 1.0<br/>print(f'{a}')</td>
  </tr>
  <tr>
    <td>a is 'text'<br/>print a</td>
    <td>a = 'text'<br/>print(f'{a}')</td>
  </tr>
  <tr>
    <td>sleep</td>
    <td>time.sleep(1)</td>
  </tr>
  <tr>
    <td>sleep 1</td>
    <td>time.sleep(1)</td>
  </tr>
  <tr>
    <td>x is ask 'y'<br>print x</td>
    <td>x = input('y')<br>try:<br>&emsp;&emsp;x = int(x)<br>except ValueError:<br/>&emsp;&emsp;x = float(x)<br>&emsp;&emsp;except ValueError:<br/>&emsp;&emsp;&emsp;&emsp;pass<br/>print(x)</td>
  </tr>
  <tr>
    <td>x is 'a', 'b', 'c'<br>print x at random</td>
    <td>x = ['a', 'b', 'c']<br>print(random.choice(x))</td>
  </tr>
  <tr>
    <td>a is 1, 2, 3<br/>f is 4<br/>add f to a</td>
    <td>a = [1, 2, 3]<br/>f = 4<br/>a.append(f)</td>
  </tr>
  <tr>
    <td>a is 1, 2, 3<br/>f is 4<br/>remove f from a</td>
    <td>a = [1, 2, 3]<br/>f = 4<br/>try:<br/>&emsp;&emsp;a.remove(f)<br/>except:<br/>&emsp;&emsp;pass</td>
  </tr>
  <tr>
    <td>a is 1, 2, 3<br/>f is 4<br/>remove f from a</td>
    <td>a = [1, 2, 3]<br/>f = 4<br/>try:<br/>&emsp;&emsp;a.remove(f)<br/>except:<br/>&emsp;&emsp;pass</td>
  </tr>
  <tr>
    <td>name is 'Hedy'<br/>if name is 'Hedy'<br/>&emsp;&emsp;print 'great'<br/>else<br/>&emsp;&emsp;print 'fine'</td>
    <td>name = 'Hedy'<br/>if name == 'Hedy':<br/>&emsp;&emsp;print(f'great')<br/>else:<br/>&emsp;&emsp;print(f'fine')</td>
  </tr>
  <tr>
    <td>name is 'Hedy'<br/>if name is 'hedy' (or | and) name is 'Hedy'<br/>&emsp;&emsp;print 'great'<br/>else<br/>&emsp;&emsp;print 'fine'</td>
    <td>name = 'Hedy'<br/>if str(name) == str('Hedy') (or | and) str(name) == str('hedy'):<br/>&emsp;&emsp;print(f'great')<br/>else:<br/>&emsp;&emsp;print(f'fine')</td>
  </tr>
  <tr>
    <td>a is 1<br/>if a (< | <= | > | >= | !=) 2<br/>&emsp;&emsp;print a</td>
    <td>a = 1<br/>if str(a).zfill(100) (< | <= | > | >= | !=) str('2').zfill(100):<br/>&emsp;&emsp;print(f'{a}')</td>
  </tr>
  <tr>
    <td>items is 'red', 'green'<br/>selected is 'red'<br/>if selected in items<br/>&emsp;&emsp;print 'found!'</td>
    <td>items = ['red', 'green']<br/>selected = 'red'<br/>if selected in items:<br/>&emsp;&emsp;print(f'found!')</td>
  </tr>
  <tr>
    <td>ns is 1, 2, 3<br/>for n in ns<br/>&emsp;&emsp;print n</td>
    <td>ns = [1, 2, 3]<br/>for n in ns:<br/>&emsp;&emsp;print(f'{n}')</td> 
  </tr>
  <tr>
    <td>for a in range 2 to 4<br/>&emsp;&emsp;a is a + 2</td>
    <td>step = 1 if int(2) < int(4) else -1<br/>for a in range(int(2), int(4) + step, step):<br/>&emsp;&emsp;a = a + 2</td>
</tr>
</tbody>
</table>


#### Incorrect Programs

<table>
<thead>
  <tr>
    <th>Hedy</th>
    <th>Exception</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td>print</td>
    <td>Incomplete Exception</td>
  </tr>
  <tr>
    <td>print'x'</td>
    <td>Invalid command</td>
  </tr>
  <tr>
    <td>print 1,0 + 1</td>
    <td>Invalid Command (TODO: this could be improved)</td>
  </tr>
  <tr>
    <td>ask</td>
    <td>Incomplete Exception</td>
  </tr>
    <tr>
    <td>(ask | print) (any text without quotes around it)</td>
    <td>Unquoted Text Exception</td>
  </tr>
  <tr>
    <td>(not (print | ask)) (any text) (not is) (any text)?</td>
    <td>Invalid Exception</td>
  </tr>
  <tr>
    <td>_SPACE (print | ask) (any text)?</td>
    <td>Invalid space</td>
  </tr>
  <tr>
    <td>_SPACE (any text) is (any text)?</td>
    <td>Invalid space</td>
  </tr>
  <tr>
    <td>a is 1, 2, 3<br/>answer is ask 'Is the number in ' a</td>
    <td>Invalid Argument Type Exception</td>
  </tr>
  <tr>
    <td>a is 1, 2, 3<br/>f is 4<br/>(add | remove) a (to | from) f</td>
    <td>Invalid Argument Type Exception</td>
  </tr>
  <tr>
    <td>items is 1, 2, 3<br/>print items</td>
    <td>Invalid Argument Type Exception</td>
  </tr>
  <tr>
    <td>a is 'test'<br/>print a + 1</td>
    <td>Invalid Argument Type Exception</td>
  </tr>
  <tr>
    <td>a is 'text'<br/>one is 1<br/>if one in a<br/>&emsp;&emsp;print 'found!'</td>
    <td>Invalid Argument Type Exception</td>
  </tr>
  <tr>
    <td>name is 1, 2<br/>if '1' is name<br/>&emsp;&emsp;print 'found'</td>
    <td>Invalid Argument Type Exception</td>
  </tr>
  <tr>
    <td>if '1' < 3<br/>&emsp;&emsp;print 'true'</td>
    <td>Invalid Argument Type Exception</td>
  </tr>
  <tr>
    <td>for a in range 1 to 10<br/>print 'hello!'</td>
    <td>No Indentation Exception</td>
  </tr>
</tbody>
</table>


## Level 15

### Commands and types

Level 15 supports:

<table>
<thead>
  <tr>
    <th>Command</th>
    <th>Types</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td>print</td>
    <td>integer | string | float | input</td>
  </tr>
  <tr>
    <td>ask *</td>
    <td>integer | string | float | input</td>
  </tr>
  <tr>
    <td>is | = (assignment)</td>
    <td>string (before `is`) + any (after `is`)</td>
  </tr>
  <tr>
    <td>sleep</td>
    <td>empty | integer</td>
  </tr>
  <tr>
    <td>at random</td>
    <td>list</td>
  </tr>
  <tr>
    <td>add to</td>
    <td>list</td>
  </tr>
  <tr>
    <td>remove from</td>
    <td>list</td>
  </tr>
  <tr>
    <td>if</td>
    <td>boolean</td>
  </tr>
  <tr>
    <td>if else</td>
    <td>boolean</td>
  </tr>
  <tr>
    <td>in</td>
    <td>any (before `in`) + list (after `in`)</td>
  </tr>
  <tr>
    <td>for</td>
    <td>string + 'in' + list | string + 'in' + 'range' + (integer | input) + 'to' + (integer | input)</td>
  </tr>
  <tr>
    <td>and</td>
    <td>boolean (on both sides of `and`)</td>
  </tr>
  <tr>
    <td>or</td>
    <td>boolean (on both sides of `or`)</td>
  </tr>
  <tr>
    <td>< **</td>
    <td>integer | float | input</td>
  </tr>
  <tr>
    <td>> **</td>
    <td>integer | float | input</td>
  </tr>
  <tr>
    <td>== | is | = (comparison) **</td>
    <td>string | integer | float | list | input</td>
  </tr>
  <tr>
    <td>!= **</td>
    <td>string | integer | float | list | input</td>
  </tr>
  <tr>
    <td><= **</td>
    <td>integer | float | input</td>
  </tr>
  <tr>
    <td>>= **</td>
    <td>integer | float | input</td>
  </tr>
  <tr>
    <td>while</td>
    <td>boolean<td>
  </tr>
</tbody>
</table>

* \* We have to use `ask` in combination with `is`, so we get `<variablename> is ask <outputquestion>`. This way, the answer of the user will be stored in a variable.

* \*\* All comparisons need to have the same type on both sides of the command. (Except when the input type is used.)

#### Correct Programs

<table>
<thead>
  <tr>
    <th>Hedy</th>
    <th>Python</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td>print 'x' 'y'</td>
    <td>print('xy')</td>
  </tr>
  <tr>
    <td>print 1 + 1</td>
    <td>print(f'{1 + 1}')</td>
  </tr>
  <tr>
    <td>print 1 - 1</td>
    <td>print(f'{1 - 1}')</td>
  </tr>
  <tr>
    <td>print 1 * 1</td>
    <td>print(f'{1 * 1}')</td>
  </tr>
  <tr>
    <td>print 1 / 1</td>
    <td>print(f'{1 / 1}')</td>
  </tr>
   <tr>
    <td>print 1.0 + 1</td>
    <td>print(f'{1.0 / 1}')</td>
  </tr>
  <tr>
    <td>a is 1<br/>print a</td>
    <td>a = 1<br/>print(f'{a}')</td>
  </tr>
  <tr>
    <td>a is 1.0<br/>print a</td>
    <td>a = 1.0<br/>print(f'{a}')</td>
  </tr>
  <tr>
    <td>a is 'text'<br/>print a</td>
    <td>a = 'text'<br/>print(f'{a}')</td>
  </tr>
  <tr>
    <td>sleep</td>
    <td>time.sleep(1)</td>
  </tr>
  <tr>
    <td>sleep 1</td>
    <td>time.sleep(1)</td>
  </tr>
  <tr>
    <td>x is ask 'y'<br>print x</td>
    <td>x = input('y')<br>try:<br>&emsp;&emsp;x = int(x)<br>except ValueError:<br/>&emsp;&emsp;x = float(x)<br>&emsp;&emsp;except ValueError:<br/>&emsp;&emsp;&emsp;&emsp;pass<br/>print(x)</td>
  </tr>
  <tr>
    <td>x is 'a', 'b', 'c'<br>print x at random</td>
    <td>x = ['a', 'b', 'c']<br>print(random.choice(x))</td>
  </tr>
  <tr>
    <td>a is 1, 2, 3<br/>f is 4<br/>add f to a</td>
    <td>a = [1, 2, 3]<br/>f = 4<br/>a.append(f)</td>
  </tr>
  <tr>
    <td>a is 1, 2, 3<br/>f is 4<br/>remove f from a</td>
    <td>a = [1, 2, 3]<br/>f = 4<br/>try:<br/>&emsp;&emsp;a.remove(f)<br/>except:<br/>&emsp;&emsp;pass</td>
  </tr>
  <tr>
    <td>a is 1, 2, 3<br/>f is 4<br/>remove f from a</td>
    <td>a = [1, 2, 3]<br/>f = 4<br/>try:<br/>&emsp;&emsp;a.remove(f)<br/>except:<br/>&emsp;&emsp;pass</td>
  </tr>
  <tr>
    <td>name is 'Hedy'<br/>if name is 'Hedy'<br/>&emsp;&emsp;print 'great'<br/>else<br/>&emsp;&emsp;print 'fine'</td>
    <td>name = 'Hedy'<br/>if name == 'Hedy':<br/>&emsp;&emsp;print(f'great')<br/>else:<br/>&emsp;&emsp;print(f'fine')</td>
  </tr>
  <tr>
    <td>name is 'Hedy'<br/>if name is 'hedy' (or | and) name is 'Hedy'<br/>&emsp;&emsp;print 'great'<br/>else<br/>&emsp;&emsp;print 'fine'</td>
    <td>name = 'Hedy'<br/>if str(name) == str('Hedy') (or | and) str(name) == str('hedy'):<br/>&emsp;&emsp;print(f'great')<br/>else:<br/>&emsp;&emsp;print(f'fine')</td>
  </tr>
  <tr>
    <td>a is 1<br/>if a (< | <= | > | >= | !=) 2<br/>&emsp;&emsp;print a</td>
    <td>a = 1<br/>if str(a).zfill(100) (< | <= | > | >= | !=) str('2').zfill(100):<br/>&emsp;&emsp;print(f'{a}')</td>
  </tr>
  <tr>
    <td>items is 'red', 'green'<br/>selected is 'red'<br/>if selected in items<br/>&emsp;&emsp;print 'found!'</td>
    <td>items = ['red', 'green']<br/>selected = 'red'<br/>if selected in items:<br/>&emsp;&emsp;print(f'found!')</td>
  </tr>
  <tr>
    <td>ns is 1, 2, 3<br/>for n in ns<br/>&emsp;&emsp;print n</td>
    <td>ns = [1, 2, 3]<br/>for n in ns:<br/>&emsp;&emsp;print(f'{n}')</td> 
  </tr>
  <tr>
    <td>for a in range 2 to 4<br/>&emsp;&emsp;a is a + 2</td>
    <td>step = 1 if int(2) &lt; int(4) else -1<br/>for a in range(int(2), int(4) + step, step):<br/>&emsp;&emsp;a = a + 2</td>
  </tr>
  <tr>
    <td>a is 0<br/>while a < 3<br>&emsp;&emsp;a is a + 1</td>
    <td>a = 0<br/>while str(a).zfill(100)&lt;str(3).zfill(100):<br/>&emsp;&emsp;a = a + 1</td>
  </tr>
</tbody>
</table>


#### Incorrect Programs

<table>
<thead>
  <tr>
    <th>Hedy</th>
    <th>Exception</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td>print</td>
    <td>Incomplete Exception</td>
  </tr>
  <tr>
    <td>print'x'</td>
    <td>Invalid command</td>
  </tr>
  <tr>
    <td>print 1,0 + 1</td>
    <td>Invalid Command (TODO: this could be improved)</td>
  </tr>
  <tr>
    <td>ask</td>
    <td>Incomplete Exception</td>
  </tr>
    <tr>
    <td>(ask | print) (any text without quotes around it)</td>
    <td>Unquoted Text Exception</td>
  </tr>
  <tr>
    <td>(not (print | ask)) (any text) (not is) (any text)?</td>
    <td>Invalid Exception</td>
  </tr>
  <tr>
    <td>_SPACE (print | ask) (any text)?</td>
    <td>Invalid space</td>
  </tr>
  <tr>
    <td>_SPACE (any text) is (any text)?</td>
    <td>Invalid space</td>
  </tr>
  <tr>
    <td>a is 1, 2, 3<br/>answer is ask 'Is the number in ' a</td>
    <td>Invalid Argument Type Exception</td>
  </tr>
  <tr>
    <td>a is 1, 2, 3<br/>f is 4<br/>(add | remove) a (to | from) f</td>
    <td>Invalid Argument Type Exception</td>
  </tr>
  <tr>
    <td>items is 1, 2, 3<br/>print items</td>
    <td>Invalid Argument Type Exception</td>
  </tr>
  <tr>
    <td>a is 'test'<br/>print a + 1</td>
    <td>Invalid Argument Type Exception</td>
  </tr>
  <tr>
    <td>a is 'text'<br/>one is 1<br/>if one in a<br/>&emsp;&emsp;print 'found!'</td>
    <td>Invalid Argument Type Exception</td>
  </tr>
  <tr>
    <td>name is 1, 2<br/>if '1' is name<br/>&emsp;&emsp;print 'found'</td>
    <td>Invalid Argument Type Exception</td>
  </tr>
  <tr>
    <td>if '1' < 3<br/>&emsp;&emsp;print 'true'</td>
    <td>Invalid Argument Type Exception</td>
  </tr>
  <tr>
    <td>for a in range 1 to 10<br/>print 'hello!'</td>
    <td>No Indentation Exception</td>
  </tr>
</tbody>
</table>

## Level 16

### Commands and types

Level 16 supports:

<table>
<thead>
  <tr>
    <th>Command</th>
    <th>Types</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td>print</td>
    <td>integer | string | float | input | list </td>
  </tr>
  <tr>
    <td>ask *</td>
    <td>integer | string | float | input | list</td>
  </tr>
  <tr>
    <td>is | = (assignment)</td>
    <td>string (before `is`) + any (after `is`)</td>
  </tr>
  <tr>
    <td>sleep</td>
    <td>empty | integer</td>
  </tr>
  <tr>
    <td>at random</td>
    <td>list</td>
  </tr>
  <tr>
    <td>add to</td>
    <td>list</td>
  </tr>
  <tr>
    <td>remove from</td>
    <td>list</td>
  </tr>
  <tr>
    <td>if</td>
    <td>boolean</td>
  </tr>
  <tr>
    <td>if else</td>
    <td>boolean</td>
  </tr>
  <tr>
    <td>in</td>
    <td>any (before `in`) + list (after `in`)</td>
  </tr>
  <tr>
    <td>for</td>
    <td>string + 'in' + list | string + 'in' + 'range' + (integer | input) + 'to' + (integer | input)</td>
  </tr>
  <tr>
    <td>and</td>
    <td>boolean (on both sides of `and`)</td>
  </tr>
  <tr>
    <td>or</td>
    <td>boolean (on both sides of `or`)</td>
  </tr>
  <tr>
    <td>< **</td>
    <td>integer | float | input</td>
  </tr>
  <tr>
    <td>> **</td>
    <td>integer | float | input</td>
  </tr>
  <tr>
    <td>== | is | = (comparison) **</td>
    <td>string | integer | float | list | input</td>
  </tr>
  <tr>
    <td>!= **</td>
    <td>string | integer | float | list | input</td>
  </tr>
  <tr>
    <td><= **</td>
    <td>integer | float | input</td>
  </tr>
  <tr>
    <td>>= **</td>
    <td>integer | float | input</td>
  </tr>
  <tr>
    <td>while</td>
    <td>boolean<td>
  </tr>
</tbody>
</table>

* \* We have to use `ask` in combination with `is`, so we get `<variablename> is ask <outputquestion>`. This way, the answer of the user will be stored in a variable.
* \*\* All comparisons need to have the same type on both sides of the command. (Except when the input type is used.)

#### Correct Programs

<table>
<thead>
  <tr>
    <th>Hedy</th>
    <th>Python</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td>print 'x' 'y'</td>
    <td>print('xy')</td>
  </tr>
  <tr>
    <td>print 1 + 1</td>
    <td>print(f'{1 + 1}')</td>
  </tr>
  <tr>
    <td>print 1 - 1</td>
    <td>print(f'{1 - 1}')</td>
  </tr>
  <tr>
    <td>print 1 * 1</td>
    <td>print(f'{1 * 1}')</td>
  </tr>
  <tr>
    <td>print 1 / 1</td>
    <td>print(f'{1 / 1}')</td>
  </tr>
   <tr>
    <td>print 1.0 + 1</td>
    <td>print(f'{1.0 / 1}')</td>
  </tr>
  <tr>
    <td>a is 1<br/>print a</td>
    <td>a = 1<br/>print(f'{a}')</td>
  </tr>
  <tr>
    <td>a is 1.0<br/>print a</td>
    <td>a = 1.0<br/>print(f'{a}')</td>
  </tr>
  <tr>
    <td>a is 'text'<br/>print a</td>
    <td>a = 'text'<br/>print(f'{a}')</td>
  </tr>
  <tr>
    <td>sleep</td>
    <td>time.sleep(1)</td>
  </tr>
  <tr>
    <td>sleep 1</td>
    <td>time.sleep(1)</td>
  </tr>
  <tr>
    <td>x is ask 'y'<br>print x</td>
    <td>x = input('y')<br>try:<br>&emsp;&emsp;x = int(x)<br>except ValueError:<br/>&emsp;&emsp;x = float(x)<br>&emsp;&emsp;except ValueError:<br/>&emsp;&emsp;&emsp;&emsp;pass<br/>print(x)</td>
  </tr>
  <tr>
    <td>x is ['a', 'b', 'c']<br>print x at random</td>
    <td>x = ['a', 'b', 'c']<br>print(random.choice(x))</td>
  </tr>
  <tr>
    <td>a is [1, 2, 3]<br/>f is 4<br/>add f to a</td>
    <td>a = [1, 2, 3]<br/>f = 4<br/>a.append(f)</td>
  </tr>
  <tr>
    <td>a is [1, 2, 3]<br/>f is 4<br/>remove f from a</td>
    <td>a = [1, 2, 3]<br/>f = 4<br/>try:<br/>&emsp;&emsp;a.remove(f)<br/>except:<br/>&emsp;&emsp;pass</td>
  </tr>
  <tr>
    <td>a is [1, 2, 3]<br/>f is 4<br/>remove f from a</td>
    <td>a = [1, 2, 3]<br/>f = 4<br/>try:<br/>&emsp;&emsp;a.remove(f)<br/>except:<br/>&emsp;&emsp;pass</td>
  </tr>
  <tr>
    <td>name is 'Hedy'<br/>if name is 'Hedy'<br/>&emsp;&emsp;print 'great'<br/>else<br/>&emsp;&emsp;print 'fine'</td>
    <td>name = 'Hedy'<br/>if name == 'Hedy':<br/>&emsp;&emsp;print(f'great')<br/>else:<br/>&emsp;&emsp;print(f'fine')</td>
  </tr>
  <tr>
    <td>name is 'Hedy'<br/>if name is 'hedy' (or | and) name is 'Hedy'<br/>&emsp;&emsp;print 'great'<br/>else<br/>&emsp;&emsp;print 'fine'</td>
    <td>name = 'Hedy'<br/>if str(name) == str('Hedy') (or | and) str(name) == str('hedy'):<br/>&emsp;&emsp;print(f'great')<br/>else:<br/>&emsp;&emsp;print(f'fine')</td>
  </tr>
  <tr>
    <td>a is 1<br/>if a (< | <= | > | >= | !=) 2<br/>&emsp;&emsp;print a</td>
    <td>a = 1<br/>if str(a).zfill(100) (< | <= | > | >= | !=) str('2').zfill(100):<br/>&emsp;&emsp;print(f'{a}')</td>
  </tr>
  <tr>
    <td>items is ['red', 'green']<br/>selected is 'red'<br/>if selected in items<br/>&emsp;&emsp;print 'found!'</td>
    <td>items = ['red', 'green']<br/>selected = 'red'<br/>if selected in items:<br/>&emsp;&emsp;print(f'found!')</td>
  </tr>
  <tr>
    <td>ns is [1, 2, 3]<br/>for n in ns<br/>&emsp;&emsp;print n</td>
    <td>ns = [1, 2, 3]<br/>for n in ns:<br/>&emsp;&emsp;print(f'{n}')</td> 
  </tr>
  <tr>
    <td>for a in range 2 to 4<br/>&emsp;&emsp;a is a + 2</td>
    <td>step = 1 if int(2) &lt; int(4) else -1<br/>for a in range(int(2), int(4) + step, step):<br/>&emsp;&emsp;a = a + 2</td>
  </tr>
  <tr>
    <td>a is 0<br/>while a < 3<br>&emsp;&emsp;a is a + 1</td>
    <td>a = 0<br/>while str(a).zfill(100)&lt;str(3).zfill(100):<br/>&emsp;&emsp;a = a + 1</td>
  </tr>
</tbody>
</table>


#### Incorrect Programs

<table>
<thead>
  <tr>
    <th>Hedy</th>
    <th>Exception</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td>print</td>
    <td>Incomplete Exception</td>
  </tr>
  <tr>
    <td>print'x'</td>
    <td>Invalid command</td>
  </tr>
  <tr>
    <td>print 1,0 + 1</td>
    <td>Invalid Command (TODO: this could be improved)</td>
  </tr>
  <tr>
    <td>ask</td>
    <td>Incomplete Exception</td>
  </tr>
    <tr>
    <td>(ask | print) (any text without quotes around it)</td>
    <td>Unquoted Text Exception</td>
  </tr>
  <tr>
    <td>(not (print | ask)) (any text) (not is) (any text)?</td>
    <td>Invalid Exception</td>
  </tr>
  <tr>
    <td>_SPACE (print | ask) (any text)?</td>
    <td>Invalid space</td>
  </tr>
  <tr>
    <td>_SPACE (any text) is (any text)?</td>
    <td>Invalid space</td>
  </tr>
  <tr>
    <td>a is [1, 2, 3]<br/>answer is ask 'Is the number in ' a</td>
    <td>Invalid Argument Type Exception</td>
  </tr>
  <tr>
    <td>a is [1, 2, 3]<br/>f is 4<br/>(add | remove) a (to | from) f</td>
    <td>Invalid Argument Type Exception</td>
  </tr>
  <tr>
    <td>items is [1, 2, 3]<br/>print items</td>
    <td>Invalid Argument Type Exception</td>
  </tr>
  <tr>
    <td>a is 'test'<br/>print a + 1</td>
    <td>Invalid Argument Type Exception</td>
  </tr>
  <tr>
    <td>a is 'text'<br/>one is 1<br/>if one in a<br/>&emsp;&emsp;print 'found!'</td>
    <td>Invalid Argument Type Exception</td>
  </tr>
  <tr>
    <td>name is [1, 2]<br/>if '1' is name<br/>&emsp;&emsp;print 'found'</td>
    <td>Invalid Argument Type Exception</td>
  </tr>
  <tr>
    <td>if '1' < 3<br/>&emsp;&emsp;print 'true'</td>
    <td>Invalid Argument Type Exception</td>
  </tr>
  <tr>
    <td>for a in range 1 to 10<br/>print 'hello!'</td>
    <td>No Indentation Exception</td>
  </tr>
  <tr>
    <td>x is 1, 2, 3</td>
    <td>Invalid Exception (?)</td>
  </tr>
  <tr>
    <td>x is [one, two, three]</td>
    <td>Unquoted text Exception</td>
  </tr>
</tbody>
</table>

## Level 17

### Commands and types

Level 17 supports:

<table>
<thead>
  <tr>
    <th>Command</th>
    <th>Types</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td>print</td>
    <td>integer | string | float | input | list </td>
  </tr>
  <tr>
    <td>ask *</td>
    <td>integer | string | float | input | list</td>
  </tr>
  <tr>
    <td>is | = (assignment)</td>
    <td>string (before `is`) + any (after `is`)</td>
  </tr>
  <tr>
    <td>sleep</td>
    <td>empty | integer</td>
  </tr>
  <tr>
    <td>at random</td>
    <td>list</td>
  </tr>
  <tr>
    <td>add to</td>
    <td>list</td>
  </tr>
  <tr>
    <td>remove from</td>
    <td>list</td>
  </tr>
  <tr>
    <td>if</td>
    <td>boolean</td>
  </tr>
  <tr>
    <td>if else</td>
    <td>boolean</td>
  </tr>
  <tr>
    <td>elif***</td>
    <td>boolean</td>
  </tr>
  <tr>
    <td>in</td>
    <td>any (before `in`) + list (after `in`)</td>
  </tr>
  <tr>
    <td>for</td>
    <td>string + 'in' + list | string + 'in' + 'range' + (integer | input) + 'to' + (integer | input)</td>
  </tr>
  <tr>
    <td>and</td>
    <td>boolean (on both sides of `and`)</td>
  </tr>
  <tr>
    <td>or</td>
    <td>boolean (on both sides of `or`)</td>
  </tr>
  <tr>
    <td>< **</td>
    <td>integer | float | input</td>
  </tr>
  <tr>
    <td>> **</td>
    <td>integer | float | input</td>
  </tr>
  <tr>
    <td>== | is | = (comparison) **</td>
    <td>string | integer | float | list | input</td>
  </tr>
  <tr>
    <td>!= **</td>
    <td>string | integer | float | list | input</td>
  </tr>
  <tr>
    <td><= **</td>
    <td>integer | float | input</td>
  </tr>
  <tr>
    <td>>= **</td>
    <td>integer | float | input</td>
  </tr>
  <tr>
    <td>while</td>
    <td>boolean<td>
  </tr>
</tbody>
</table>

* \* We have to use `ask` in combination with `is`, so we get `<variablename> is ask <outputquestion>`. This way, the answer of the user will be stored in a variable.
* \*\* All comparisons need to have the same type on both sides of the command. (Except when the input type is used.)
* \*\*\* There has to be an `if` (with a boolean), before `elif` (with a boolean), but then, multiple times `elif` is possible. After that, using an `else` is optional.

#### Correct Programs

<table>
<thead>
  <tr>
    <th>Hedy</th>
    <th>Python</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td>print 'x' 'y'</td>
    <td>print('xy')</td>
  </tr>
  <tr>
    <td>print 1 + 1</td>
    <td>print(f'{1 + 1}')</td>
  </tr>
  <tr>
    <td>print 1 - 1</td>
    <td>print(f'{1 - 1}')</td>
  </tr>
  <tr>
    <td>print 1 * 1</td>
    <td>print(f'{1 * 1}')</td>
  </tr>
  <tr>
    <td>print 1 / 1</td>
    <td>print(f'{1 / 1}')</td>
  </tr>
   <tr>
    <td>print 1.0 + 1</td>
    <td>print(f'{1.0 / 1}')</td>
  </tr>
  <tr>
    <td>a is 1<br/>print a</td>
    <td>a = 1<br/>print(f'{a}')</td>
  </tr>
  <tr>
    <td>a is 1.0<br/>print a</td>
    <td>a = 1.0<br/>print(f'{a}')</td>
  </tr>
  <tr>
    <td>a is 'text'<br/>print a</td>
    <td>a = 'text'<br/>print(f'{a}')</td>
  </tr>
  <tr>
    <td>sleep</td>
    <td>time.sleep(1)</td>
  </tr>
  <tr>
    <td>sleep 1</td>
    <td>time.sleep(1)</td>
  </tr>
  <tr>
    <td>x is ask 'y'<br>print x</td>
    <td>x = input('y')<br>try:<br>&emsp;&emsp;x = int(x)<br>except ValueError:<br/>&emsp;&emsp;x = float(x)<br>&emsp;&emsp;except ValueError:<br/>&emsp;&emsp;&emsp;&emsp;pass<br/>print(x)</td>
  </tr>
  <tr>
    <td>x is ['a', 'b', 'c']<br>print x at random</td>
    <td>x = ['a', 'b', 'c']<br>print(random.choice(x))</td>
  </tr>
  <tr>
    <td>a is [1, 2, 3]<br/>f is 4<br/>add f to a</td>
    <td>a = [1, 2, 3]<br/>f = 4<br/>a.append(f)</td>
  </tr>
  <tr>
    <td>a is [1, 2, 3]<br/>f is 4<br/>remove f from a</td>
    <td>a = [1, 2, 3]<br/>f = 4<br/>try:<br/>&emsp;&emsp;a.remove(f)<br/>except:<br/>&emsp;&emsp;pass</td>
  </tr>
  <tr>
    <td>a is [1, 2, 3]<br/>f is 4<br/>remove f from a</td>
    <td>a = [1, 2, 3]<br/>f = 4<br/>try:<br/>&emsp;&emsp;a.remove(f)<br/>except:<br/>&emsp;&emsp;pass</td>
  </tr>
  <tr>
    <td>name is 'Hedy'<br/>if name is 'Hedy':<br/>&emsp;&emsp;print 'great'<br/>else:<br/>&emsp;&emsp;print 'fine'</td>
    <td>name = 'Hedy'<br/>if name == 'Hedy':<br/>&emsp;&emsp;print(f'great')<br/>else:<br/>&emsp;&emsp;print(f'fine')</td>
  </tr>
  <tr>
    <td>name is 'Hedy'<br/>if name is 'hedy' (or | and) name is 'Hedy':<br/>&emsp;&emsp;print 'great'<br/>else:<br/>&emsp;&emsp;print 'fine'</td>
    <td>name = 'Hedy'<br/>if str(name) == str('Hedy') (or | and) str(name) == str('hedy'):<br/>&emsp;&emsp;print(f'great')<br/>else:<br/>&emsp;&emsp;print(f'fine')</td>
  </tr>
  <tr>
    <td>name is 'Hedy'<br/>if name is 'hedy' (or | and) name is 'Hedy':<br/>&emsp;&emsp;print 'great'<br/>elif name is 'Felienne':<br/>&emsp;&emsp;print 'lovely!'<br/>elif name is 'Julia':<br/>&emsp;&emsp;print 'Oh that is the most popular baby name in the Netherlands!'<br/>else:<br/>&emsp;&emsp;print 'fine'</td>
    <td>name = 'Hedy'<br/>if str(name) == str('Hedy') (or | and) str(name) == str('hedy'):<br/>&emsp;&emsp;print(f'great')<br/>else:<br/>&emsp;&emsp;print(f'fine')</td>
  </tr>
  <tr>
    <td>a is 1<br/>if a (< | <= | > | >= | !=) 2:<br/>&emsp;&emsp;print a</td>
    <td>a = 1<br/>if str(a).zfill(100) (< | <= | > | >= | !=) str('2').zfill(100):<br/>&emsp;&emsp;print(f'{a}')</td>
  </tr>
  <tr>
    <td>items is ['red', 'green']<br/>selected is 'red'<br/>if selected in items:<br/>&emsp;&emsp;print 'found!'</td>
    <td>items = ['red', 'green']<br/>selected = 'red'<br/>if selected in items:<br/>&emsp;&emsp;print(f'found!')</td>
  </tr>
  <tr>
    <td>ns is [1, 2, 3]<br/>for n in ns<br/>&emsp;&emsp;print n</td>
    <td>ns = [1, 2, 3]<br/>for n in ns:<br/>&emsp;&emsp;print(f'{n}')</td> 
  </tr>
  <tr>
    <td>for a in range 2 to 4:<br/>&emsp;&emsp;a is a + 2</td>
    <td>step = 1 if int(2) &lt; int(4) else -1<br/>for a in range(int(2), int(4) + step, step):<br/>&emsp;&emsp;a = a + 2</td>
  </tr>
  <tr>
    <td>a is 0<br/>while a < 3:<br>&emsp;&emsp;a is a + 1</td>
    <td>a = 0<br/>while str(a).zfill(100)&lt;str(3).zfill(100):<br/>&emsp;&emsp;a = a + 1</td>
  </tr>
</tbody>
</table>


#### Incorrect Programs

<table>
<thead>
  <tr>
    <th>Hedy</th>
    <th>Exception</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td>print</td>
    <td>Incomplete Exception</td>
  </tr>
  <tr>
    <td>print'x'</td>
    <td>Invalid command</td>
  </tr>
  <tr>
    <td>print 1,0 + 1</td>
    <td>Invalid Command (TODO: this could be improved)</td>
  </tr>
  <tr>
    <td>ask</td>
    <td>Incomplete Exception</td>
  </tr>
    <tr>
    <td>(ask | print) (any text without quotes around it)</td>
    <td>Unquoted Text Exception</td>
  </tr>
  <tr>
    <td>(not (print | ask)) (any text) (not is) (any text)?</td>
    <td>Invalid Exception</td>
  </tr>
  <tr>
    <td>_SPACE (print | ask) (any text)?</td>
    <td>Invalid space</td>
  </tr>
  <tr>
    <td>_SPACE (any text) is (any text)?</td>
    <td>Invalid space</td>
  </tr>
  <tr>
    <td>a is [1, 2, 3]<br/>answer is ask 'Is the number in ' a</td>
    <td>Invalid Argument Type Exception</td>
  </tr>
  <tr>
    <td>a is [1, 2, 3]<br/>f is 4<br/>(add | remove) a (to | from) f</td>
    <td>Invalid Argument Type Exception</td>
  </tr>
  <tr>
    <td>items is [1, 2, 3]<br/>print items</td>
    <td>Invalid Argument Type Exception</td>
  </tr>
  <tr>
    <td>a is 'test'<br/>print a + 1</td>
    <td>Invalid Argument Type Exception</td>
  </tr>
  <tr>
    <td>a is 'text'<br/>one is 1<br/>if one in a<br/>&emsp;&emsp;print 'found!'</td>
    <td>Invalid Argument Type Exception</td>
  </tr>
  <tr>
    <td>name is [1, 2]<br/>if '1' is name<br/>&emsp;&emsp;print 'found'</td>
    <td>Invalid Argument Type Exception</td>
  </tr>
  <tr>
    <td>if '1' < 3:<br/>&emsp;&emsp;print 'true'</td>
    <td>Invalid Argument Type Exception</td>
  </tr>
  <tr>
    <td>for a in range 1 to 10:<br/>print 'hello!'</td>
    <td>No Indentation Exception</td>
  </tr>
  <tr>
    <td>x is 1, 2, 3</td>
    <td>Invalid Exception (?)</td>
  </tr>
  <tr>
    <td>x is [one, two, three]</td>
    <td>Unquoted text Exception</td>
  </tr>
  <tr>
    <td>(if | for | while) (boolean) (newline without ':' first) </td>
    <td>Invalid Exception</td>
  </tr>
  <tr>
    <td>(any lines with code without `if`) elif (boolean):</td>
    <td>Invalid Exception</td>
  </tr>
</tbody>
</table>