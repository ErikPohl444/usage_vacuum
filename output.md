```
    logger.info("demoing setsy class")
    x = setsy([(1, 2), (1, 3)])
    b = setsy([6, 7, 8])
    print('here', list(b.powerset()))
```
here [(6,), (8, 7), (8,), (6, 7), (7,), (8, 6), (8, 6, 7), ()]
```
    print(x.issubset(b))
```
False
```
    print(x.issuperset(b))
```
False
```
    x = x.union(b)  # class setsy which inherits from set returns a set from union
    print(x)
```
{(1, 2), 6, 7, 8, (1, 3)}
```
    print(type(x))
```
<class 'src.setsy.setsy'>
```
    y = {6, 5, 2, 1}
    print('------------')
```
------------
```
    print(x.cartesian(y))
```
{((1, 2), 2), ((1, 2), 5), (8, 6), ((1, 3), 1), (6, 2), (7, 1), (6, 5), ((1, 2), 1), (8, 2), (8, 5), (6, 1), ((1, 3), 6), (7, 6), (8, 1), ((1, 2), 6), ((1, 3), 2), ((1, 3), 5), (7, 2), (6, 6), (7, 5)}
```
    print("is not subset attempt")
```
is not subset attempt
```
    a = setsy([1, 2, 3])
    print("a:", a)
```
a: {1, 2, 3}
```
    b = setsy([2, 3, 4, 5, 6, 7])
    print("b:", b)
```
b: {2, 3, 4, 5, 6, 7}
```
    c = a.is_not_subset(b)
    print("result of a.is_not_subset(b): ", c)
```
result of a.is_not_subset(b):  {1}
```
    if c:
        print("a is not a subset of b")
```
a is not a subset of b
```
    print("is not superset attempt")
```
is not superset attempt
```
    a = setsy([1, 2, 3])
    print("a:", a)
```
a: {1, 2, 3}
```
    b = setsy([2, 3, 4, 5, 6, 7])
    print("b:", b)
```
b: {2, 3, 4, 5, 6, 7}
```
    c = b.is_not_superset(a)
    print("result of b.is_not_superset(a): ", c)
```
result of b.is_not_superset(a):  {1}
```
    if c:
        print("b is not a superset of a")
```
b is not a superset of a
```
    print("is not subset attempt")
```
is not subset attempt
```
    a = setsy([2, 3])
    print("a:", a)
```
a: {2, 3}
```
    b = setsy([2, 3, 4, 5, 6, 7])
    print("b:", b)
```
b: {2, 3, 4, 5, 6, 7}
```
    c = a.is_not_subset(b)
    print("result of a.is_not_subset(b): ", c)
```
result of a.is_not_subset(b):  {}
```
    print("a is not a subset of b") if c else print("a is a subset of b")
```
a is a subset of b
```
    print("is not superset attempt")
```
is not superset attempt
```
    a = setsy([2, 3])
    print("a:", a)
```
a: {2, 3}
```
    b = setsy([2, 3, 4, 5, 6, 7])
    print("b:", b)
```
b: {2, 3, 4, 5, 6, 7}
```
    c = b.is_not_superset(a)
    print("result of b.is_not_superset(a): ", c)
```
result of b.is_not_superset(a):  {}
```
    if c:
    print("is not subset attempt")
```
is not subset attempt
```
    a = setsy([2, 3])
    print("a:", a)
```
a: {2, 3}
```
    b = setsy([2])
    print("b:", b)
```
b: {2}
```
    c = a.is_not_subset(b)
    print("result of a.is_not_subset(b): ", c)
```
result of a.is_not_subset(b):  {3}
```
    print("a is not a subset of b") if c else print("a is a subset of b")
```
a is not a subset of b
```
    print("is not superset attempt")
```
is not superset attempt
```
    a = setsy([2, 3])
    print("a:", a)
```
a: {2, 3}
```
    b = setsy([2])
    print("b:", b)
```
b: {2}
```
    c = b.is_not_superset(a)
    print("result of b.is_not_superset(a): ", c)
```
result of b.is_not_superset(a):  {3}
```
    if c:
        print("b is not a superset of a")
```
b is not a superset of a
