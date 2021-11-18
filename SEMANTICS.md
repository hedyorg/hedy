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
    <td>print x</td>
    <td>print('x')</td>
  </tr>
  <tr>
    <td>forward</td>
    <td>t = turtle.Turtle()<br>t.forward(50)</td>
  </tr>
  <tr>
    <td>turn</td>
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
    <td>echo</td>
    <td>Incomplete Exception</td>
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
    <td>print x</td>
    <td>print('x')</td>
  </tr>
  <tr>
    <td>forward</td>
    <td>t = turtle.Turtle()<br>t.forward(50)</td>
  </tr>
  <tr>
    <td>turn</td>
    <td>t = turtle.Turtle()<br>t.right(90)</td>
  </tr>
  <tr>
    <td>ask x</td>
    <td>answer = input('x')</td>
  </tr>
  <tr>
    <td>x is ask y<br>print x</td>
    <td>x = input('y')<br>print(x)</td>
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
* `at random`
* `add to` (soon)
* `remove from` (soon)

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
    <td>print x</td>
    <td>print('x')</td>
  </tr>
  <tr>
    <td>forward</td>
    <td>t = turtle.Turtle()<br>t.forward(50)</td>
  </tr>
  <tr>
    <td>turn</td>
    <td>t = turtle.Turtle()<br>t.right(90)</td>
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
    <td>x is a, b, c<br>print x at random</td>
    <td>x = ['a', 'b', 'c']<br>print(random.choice(x))</td>
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
* `at random`

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
    <td>print 'x'</td>
    <td>print('x')</td>
  </tr>
  <tr>
    <td>forward</td>
    <td>t = turtle.Turtle()<br>t.forward(50)</td>
  </tr>
  <tr>
    <td>turn</td>
    <td>t = turtle.Turtle()<br>t.right(90)</td>
  </tr>
  <tr>
    <td>ask 'x'</td>
    <td>answer = input('x')</td>
  </tr>
  <tr>
    <td>x is ask 'y'<br>print x</td>
    <td>x = input('y')<br>print(x)</td>
  </tr>
  <tr>
    <td>x is a, b, c<br>print x at random</td>
    <td>x = ['a', 'b', 'c']<br>print(random.choice(x))</td>
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
</tbody>
</table>
