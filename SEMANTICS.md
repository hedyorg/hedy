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
    <td>(print | ask | forward | turn | echo) (any text)?</td>
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
 


