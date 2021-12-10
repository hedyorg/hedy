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
    <td>turn 100</td>
    <td>t = turtle.Turtle()<br>t.right(100)</td>
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
    <td>echo</td>
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

### Commands

Level 2 supports:
* `print`
* `ask`
* `forward`
* `turn`
* `is`
* `sleep`

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

### Commands

Level 3 supports:
* `print`
* `ask`
* `forward`
* `turn`
* `is`
* `sleep`
* `at random`
* `add to`
* `remove from`

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

### Commands

Level 4 supports:
* `print`
* `ask`
* `forward`
* `turn`
* `is`
* `sleep`
* `at random`
* `add to`
* `remove from`

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

### Commands

Level 5 supports:
* `print`
* `ask`
* `forward`
* `turn`
* `is`
* `sleep`
* `at random`
* `add to`
* `remove from`
* `if`
* `if else`

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
    <td>naam = 'Hedy'<br/>if name == 'Hedy':<br/>&emsp;&emsp;print(f'great')<br/>else:<br/>&emsp;&emsp;print(f'fine')</td>
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

### Commands

Level 6 supports:
* `print`
* `ask`
* `forward`
* `turn`
* `is`
* `sleep`
* `at random`
* `add to`
* `remove from`
* `if`
* `if else`

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
    <td>naam = 'Hedy'<br/>if name == 'Hedy':<br/>&emsp;&emsp;print(f'great')<br/>else:<br/>&emsp;&emsp;print(f'fine')</td>
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

### Commands

Level 7 supports:
* `print`
* `ask`
* `forward`
* `turn`
* `is`
* `sleep`
* `at random`
* `add to`
* `remove from`
* `if`
* `if else`
* `repeat`

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
    <td>naam = 'Hedy'<br/>if name == 'Hedy':<br/>&emsp;&emsp;print(f'great')<br/>else:<br/>&emsp;&emsp;print(f'fine')</td>
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
* `print`
* `ask`
* `forward`
* `turn`
* `is`
* `sleep`
* `at random`
* `add to`
* `remove from`
* `if`
* `if else`
* `repeat`

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
    <td>naam = 'Hedy'<br/>if name == 'Hedy':<br/>&emsp;&emsp;print(f'great')<br/>else:<br/>&emsp;&emsp;print(f'fine')</td>
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

### Commands

Level 9 supports:
* `print`
* `ask`
* `forward`
* `turn`
* `is`
* `sleep`
* `at random`
* `add to`
* `remove from`
* `if`
* `if else`
* `repeat`

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
    <td>naam = 'Hedy'<br/>if name == 'Hedy':<br/>&emsp;&emsp;print(f'great')<br/>else:<br/>&emsp;&emsp;print(f'fine')</td>
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

### Commands

Level 10 supports:
* `print`
* `ask`
* `forward`
* `turn`
* `is`
* `sleep`
* `at random`
* `add to`
* `remove from`
* `if`
* `if else`
* `repeat`
* `for`

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
    <td>naam = 'Hedy'<br/>if name == 'Hedy':<br/>&emsp;&emsp;print(f'great')<br/>else:<br/>&emsp;&emsp;print(f'fine')</td>
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

### Commands

Level 11 supports:
* `print`
* `ask`
* `is`
* `sleep`
* `at random`
* `add to`
* `remove from`
* `if`
* `if else`
* `repeat`
* `for`

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
    <td>naam = 'Hedy'<br/>if name == 'Hedy':<br/>&emsp;&emsp;print(f'great')<br/>else:<br/>&emsp;&emsp;print(f'fine')</td>
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

### Commands

Level 12 supports:
* `print`
* `ask`
* `is`
* `sleep`
* `at random`
* `add to`
* `remove from`
* `if`
* `if else`
* `repeat`
* `for`

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
    <td>x is a, b, c<br>print x at random</td>
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
    <td>name is Hedy<br/>if name is Hedy<br/>&emsp;&emsp;print 'great'<br/>else<br/>&emsp;&emsp;print 'fine'</td>
    <td>naam = 'Hedy'<br/>if name == 'Hedy':<br/>&emsp;&emsp;print(f'great')<br/>else:<br/>&emsp;&emsp;print(f'fine')</td>
  </tr>
  <tr>
    <td>items is red, green<br/>selected is red<br/>if selected in items<br/>&emsp;&emsp;print 'found!'</td>
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

### Commands

Level 13 supports:
* `print`
* `ask`
* `is`
* `sleep`
* `at random`
* `add to`
* `remove from`
* `if`
* `if else`
* `repeat`
* `for`

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
    <td>x is a, b, c<br>print x at random</td>
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
    <td>name is Hedy<br/>if name is Hedy<br/>&emsp;&emsp;print 'great'<br/>else<br/>&emsp;&emsp;print 'fine'</td>
    <td>naam = 'Hedy'<br/>if name == 'Hedy':<br/>&emsp;&emsp;print(f'great')<br/>else:<br/>&emsp;&emsp;print(f'fine')</td>
  </tr>
  <tr>
    <td>name is Hedy<br/>if name is hedy (or | and) name is Hedy<br/>&emsp;&emsp;print 'great'<br/>else<br/>&emsp;&emsp;print 'fine'</td>
    <td>naam = 'Hedy'<br/>if str(name) == str('Hedy') (or | and) str(name) == str('hedy'):<br/>&emsp;&emsp;print(f'great')<br/>else:<br/>&emsp;&emsp;print(f'fine')</td>
  </tr>
  <tr>
    <td>items is red, green<br/>selected is red<br/>if selected in items<br/>&emsp;&emsp;print 'found!'</td>
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

### Commands

Level 14 supports:
* `print`
* `ask`
* `is`
* `sleep`
* `at random`
* `add to`
* `remove from`
* `if`
* `if else`
* `repeat`
* `for`

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
    <td>x is a, b, c<br>print x at random</td>
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
    <td>name is Hedy<br/>if name is Hedy<br/>&emsp;&emsp;print 'great'<br/>else<br/>&emsp;&emsp;print 'fine'</td>
    <td>naam = 'Hedy'<br/>if name == 'Hedy':<br/>&emsp;&emsp;print(f'great')<br/>else:<br/>&emsp;&emsp;print(f'fine')</td>
  </tr>
  <tr>
    <td>name is Hedy<br/>if name is hedy (or | and) name is Hedy<br/>&emsp;&emsp;print 'great'<br/>else<br/>&emsp;&emsp;print 'fine'</td>
    <td>naam = 'Hedy'<br/>if str(name) == str('Hedy') (or | and) str(name) == str('hedy'):<br/>&emsp;&emsp;print(f'great')<br/>else:<br/>&emsp;&emsp;print(f'fine')</td>
  </tr>
  <tr>
    <td>a is 1<br/>if a (< | <= | > | >= | !=) 2<br/>&emsp;&emsp;print a</td>
    <td>a = 1<br/>if str(a).zfill(100) (< | <= | > | >= | !=) str('2').zfill(100):<br/>&emsp;&emsp;print(f'{a}')</td>
  </tr>
  <tr>
    <td>items is red, green<br/>selected is red<br/>if selected in items<br/>&emsp;&emsp;print 'found!'</td>
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

### Commands

Level 15 supports:
* `print`
* `ask`
* `is`
* `sleep`
* `at random`
* `add to`
* `remove from`
* `if`
* `if else`
* `repeat`
* `for`
* `while`

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
    <td>x is a, b, c<br>print x at random</td>
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
    <td>name is Hedy<br/>if name is Hedy<br/>&emsp;&emsp;print 'great'<br/>else<br/>&emsp;&emsp;print 'fine'</td>
    <td>naam = 'Hedy'<br/>if name == 'Hedy':<br/>&emsp;&emsp;print(f'great')<br/>else:<br/>&emsp;&emsp;print(f'fine')</td>
  </tr>
  <tr>
    <td>name is Hedy<br/>if name is hedy (or | and) name is Hedy<br/>&emsp;&emsp;print 'great'<br/>else<br/>&emsp;&emsp;print 'fine'</td>
    <td>naam = 'Hedy'<br/>if str(name) == str('Hedy') (or | and) str(name) == str('hedy'):<br/>&emsp;&emsp;print(f'great')<br/>else:<br/>&emsp;&emsp;print(f'fine')</td>
  </tr>
  <tr>
    <td>a is 1<br/>if a (< | <= | > | >= | !=) 2<br/>&emsp;&emsp;print a</td>
    <td>a = 1<br/>if str(a).zfill(100) (< | <= | > | >= | !=) str('2').zfill(100):<br/>&emsp;&emsp;print(f'{a}')</td>
  </tr>
  <tr>
    <td>items is red, green<br/>selected is red<br/>if selected in items<br/>&emsp;&emsp;print 'found!'</td>
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
