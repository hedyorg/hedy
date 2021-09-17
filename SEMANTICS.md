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
<tr> <th> Hedy </th> <th> Python </th> </tr>
<tr>
<td>
 
```
print x
```

</td>
<td>
 
```python
print('x')
```

</td>
</tr>
<tr>
<td>
 
```
forward
```

</td>
<td>
 
```python
t = turtle.Turtle()
t.forward(50)
```
 
</td>
</tr>
<tr>
<td>
 
```
turn
```

</td>
<td>
 
```python
t = turtle.Turtle()
t.right(90)
```
 
</td>
</tr>
<tr>
<td>
 
```
ask x
```

</td>
<td>
 
```python
answer = input('x')
```
 
</td>
</tr>
<tr>
<td>
 
```
ask x
```

</td>
<td>
 
```python
answer = input('x')
```
 
</td>
</tr>
<tr>
<td>
 
```
ask x
echo y
```

</td>
<td>
 
```python
answer = input('x')
print('y', answer)
```
 
</td>
</tr>
</table>


 

#### Incorrect Programs

* print -> Incomplete Exception
* ask -> Incomplete Exception
* echo -> Incomplete Exception
* words other than print, ask, forward, turn, echo -> Invaid Exception
* echo x -> Lonely echo Exception


