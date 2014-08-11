
churry
====

Warning
----

This library does not comply with the Python philosophy **TIOOTDI**.
Leave before you faint.

Introduction
----

The word churry is the combination of **chain and curry**,
which implies that the library named as such does the same.

Affirmative to that.
This library enables you to make a function chainable and curriable.

chainability
----

Suppose we have a function:

```python
def move(ball, from_=0, to=10):
    pass
```

Normally, we would

```python
move(spam, 1, 5)
# or
move(spam, from_=1, to=5)
```

Now, with the churry decorator

```python
from churry import churried

@churried()
def move(ball, from_=0, to=10):
    pass
```

we can

```python
move.from_(1).to(5)(spam)
```

Note that for functions with variable arguments (both positional or keyword),
churry wouldn't know when to stop receiving arguments.
So you have to call the churried function with empty argument to inform churry
that it's time to evaluate. For example,

```python
@churried()
def move_simultaneously(*balls, from_=0, to=10)
    pass

move_simultaneously(foo, bar).from_(1).to(5)()
# or
move_simultaneously.from_(1).to(5)(foo, bar)()
```

curriability
----

With churry, you can

```python
move_to_1_5 = move_simultaneously.from_(1).to(5).freeze()

move_to_1_5(foo, bar)()
move_to_1_5(bar, foo)()
move_to_1_5(spam, ham)()
```

If you set `auto_restore` to `False`, you may need to call `restore()`
manually each time you evaluate a churried function.

I may have wrongly used the terms _chain_ and _curry_, but that's not important
(at least to me). What's important now is that you can **churry** a function.

Gotchas
----

If the function you want to decorate does not have variable positional or
variable keyword argument, you must supply the keyword arguments before the
positional arguments are supplied.
Because when positional arguments are fully supplied, churry evaluates the
function with the default argument values.

In short, do

```python
move.from_(1).to(5)(spam)
# or
move.to(5).from_(1)(spam)
```

**Do not**

```python
move(spam).from_(1).to(5)
# this raises AttributeError because NoneType (return value of move(spam))
# does not have attribute 'from_'
```

If you do not want this feature (or whatever it is), use the `explicit` switch
so that churry only does evaluation after you call it with empty argument.

Examples
----

See `tests.py`

License
----

This library is licensed under GPLv3.
