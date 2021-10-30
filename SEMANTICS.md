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
 

## Level 2

### Commands

In Level 2 variables and the keyword `is` are added, they keyword `echo` is removed, and `print` and `ask` change their syntax. Thus, this level supports:

* `print`

* `ask`

* `forward`

* `turn`

* `ask`

* variables  


### Correct Programs

<table>
<thead>
  <tr>
    <th>Hedy</th>
    <th>Python</th>
  </tr>
</thead>
<tbody>
	<tr>
		<td>
<pre>
name is Hedy
print Welcome name
</pre>
        </td>
		<td>
<pre>
name = 'Hedy'
print(f'Welcome {name}')
</pre>           
        </td>
    </tr>
    <tr>
		<td>
<pre>
answer is ask What is your name?
print answer
</pre>
        </td>
		<td>
<pre>
answer = input('What is your name'+'?')
print(f'{answer}')
</pre>           
        </td>
    </tr>
        <tr>
		<td>
<pre>
angle is 90
turn angle
forward angle
</pre>
        </td>
		<td>
<pre>
t = turtle.Turtle()
angle = '90'
t.right(angle)
t.forward(angle)
time.sleep(0.1)
</pre>           
        </td>
    </tr>	
</tbody>
</table>
