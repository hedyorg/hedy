## LEVEL 11
Functions without arguments nor return
```
define fruit
    print "fruit"
    call fruit_2
    print "fruit"

define fruit_2
    print "fruit2"
    
for i in range 1 to 3
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
    print "fruit2: " y " " x
    
f = 'C'
g = 4.0
call fruit with 5 + 4.4, "A", f, g
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