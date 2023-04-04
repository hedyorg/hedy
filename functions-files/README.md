## LEVEL 11
Functions without arguments nor return
```
define fruit
    print "fruit"
    call fruit_2
    print "fruit"

define fruit_2
    print "fruit2"
    
call fruit
```

## LEVEL 12
Functions with arguments
```
define fruit using a, b, c, d
    print "fruit " c
    call fruit_2 with a, d
    print "fruit " b

define fruit_2 using x, y
    print "fruit2: " x " " y
    
f = 'C'
g = 4.0
call fruit with 100, "A", f, g
```

## LEVEL 14
Functions with arguments and return
```
define squares using a
    return a * a


num = 7
print call squares with num

print call squares with 3.3
```

## Bugs
- cannot return inside if/else statement yet

- Calling a function inside a print with a quoted text argument does not work

- Cannot return expressions / String concatenation yet