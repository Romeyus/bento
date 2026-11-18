# Option

```python
type Option[T] = Some[T] | Nothing
```

The `Option` type is a union of `Some` and `Nothing`, where `Some` represents the presence of a value and `Nothing` represents its absence.

## Variants

### Nothing

```python
class Nothing:
    def __init__(self) -> None: ...
```

Does not contains a value.

### Some

```python
class Some[T]:
    def __init__(self, value: T) -> None: ...
```

Contains a value of type `T`.

## Methods

### and_

```python
def and_[U](self, optb: Option[U]) -> Option[U]: ...
```

Returns `optb` if `self` is a `Some`, otherwise returns `self`.

Arguments passed to `and_` are eagerly evaluated. If you are passing the product of a function, we recommend using [`and_then`](#and_then) which is lazily evaluated.

**Examples**

```python
from bento import Nothing, Option, Some

x = Some(2)
y: Option[str] = Nothing()
assert x.and_(y) == Nothing()

x: Option[int] = Nothing()
y = Some("foo")
assert x.and_(y) == Nothing()

x = Some(2)
y = Some("foo")
assert x.and_(y) == Some("foo")

x: Option[int] = Nothing()
y: Option[str] = Nothing()
assert x.and_(y) == Nothing()
```

### and_then

```python
def and_then[U](self, f: Callable[[T], Option[U]]) -> Option[U]: ...
```

Returns the `f` product if `self` is a `Some`, otherwise returns `self`.

The `f` product is the return value of `f` when called with the contained value.

**Examples**

```python
from bento import Nothing, Option, Some

def sq_then_to_str(x: int) -> Option[str]:
    if x >= 1_000_000: # simulate an overflow
        return Nothing()
    return Some(x**2).map(str)

assert Some(2).and_then(sq_then_to_str) == Some("4")
assert Some(1_000_000).and_then(sq_then_to_str) == Nothing()
assert Nothing().and_then(sq_then_to_str) == Nothing()
```

### expect

```python
def expect(self, msg: str) -> T: ...
```

Returns the contained value.

**Raises**

If `self` is a `Nothing`, raises an `UnwrapError` containing `msg`.

**Examples**

```python
from bento import Nothing, Option, Some

x = Some("value")
assert x.expect("value should be present") == "value"

y: Option[str] = Nothing()
y.expect("value should be present") # raises an UnwrapError containing 'value should be present'
```

### filter

```python
def filter(self, predicate: Callable[[T], bool]) -> Option[T]: ...
```

Returns `self` if `self` is a `Nothing`, otherwise returns:

- `self` if the `predicate` product is `True`, or
- a `Nothing` if the `predicate` product is `False`

**Examples**

```python
from bento import Nothing, Option, Some

def is_even(n: int) -> bool:
    return n % 2 == 0

assert Nothing().filter(is_even) == Nothing()
assert Some(4).filter(is_even) == Some(4)
assert Some(3).filter(is_even) == Nothing()
```

### map

```python
def map[U](self, f: Callable[[T], U]) -> Option[U]: ...
```

Returns a `Some` containing the `f` product if `self` is a `Some`, otherwise returns `self`.

**Examples**

Maps a string to an integer by measuring its length.

```python
from bento import Nothing, Option, Some

x = Some("Hello world!")
assert x.map(len) == Some(12)

y: Option[str] = Nothing()
assert y.map(len) == Nothing()
```

### map_or

```python
def map_or[U](self, default: U, f: Callable[[T], U]) -> U: ...
```

Returns the `f` product if `self` is a `Some`, otherwise returns `default`.

Arguments passed to `map_or` are eagerly evaluated. If you are passing the product of a function, we recommend using [`map_or_else`](#map_or_else) which is lazily evaluated.

**Examples**

```python
from bento import Nothing, Option, Some

x = Some("foo")
assert x.map_or(42, len) == 3

y: Option[str] = Nothing()
assert y.map_or(42, len) == 42
```

### map_or_else

```python
def map_or_else[U](self, default: Callable[[], U], f: Callable[[T], U]) -> U: ...
```

Returns the `f` product is `self` is a `Some`, otherwise returns the `default` product.

**Examples**

```python
from bento import Nothing, Option, Some

k = 21

x = Some("foo")
assert x.map_or_else(lambda: k * 2, len) == 3

y: Option[str] = Nothing()
assert y.map_or_else(lambda: k * 2, len) == 42
```

### ok_or

```python
def ok_or[E](self, e: E) -> Result[T, E]: ...
```

Returns an `Ok` containing `self.value` if `self` is a `Some`, otherwise returns an `Err` containing `e`.

Arguments passed to `ok_or` are eagerly evaluated. If you are passing the product of a function, we recommend using [`ok_or_else`](#ok_or_else) which is lazily evaluated.

**Examples**

```python
from bento import Err, Nothing, Ok, Option, Some

x = Some("foo")
assert x.ok_or(0) == Ok("foo")

y: Option[str] = Nothing()
assert y.ok_or(0) == Err(0)
```

### ok_or_else

Returns an `Ok` containing `self.value` if `self` is a `Some`, otherwise returns an `Err` containing the `f` product.

**Examples**

```python
from bento import Err, Nothing, Ok, Option, Some

x = Some("foo")
assert x.ok_or_else(lambda: 0) == Ok("foo")

y: Option[str] = Nothing()
assert y.ok_or_else(lambda: 0) == Err(0)
```

### or_

```python
def or_(self, optb: Option[T]) -> Option[T]: ...
```

Returns `optb` is `self` is a `Nothing`, otherwise returns `self`.

Arguments passed to `or_` are eagerly evaluated. If you are passing the product of a function, we recommend using [`or_else`](#or_else) which is lazily evaluated.

**Examples**

```python
from bento import Nothing, Option, Some

x = Some(2)
y = Nothing()
assert x.or_(y) == Some(2)

x = Nothing()
y = Some(100)
assert x.or_(y) == Some(100)

x = Some(2)
y = Some(100)
assert x.or_(y) == Some(2)

x = Nothing()
y = Nothing()
assert x.or_(y) == Nothing()
```

### or_else

```python
def or_else(self, f: Callable[[], Option[T]]) -> Option[T]: ...
```

Returns the `f` product if `self` is a `Nothing`, otherwise returns `self`.

**Examples**

```python
from bento import Nothing, Option, Some

def nobody() -> Option[str]:
    return Nothing()

def vikings() -> Option[str]:
    return Some("vikings")

assert Some("barbarians").or_else(vikings) == Some("barbarians")
assert Nothing().or_else(vikings) == Some("vikings")
assert Nothing().or_else(nobody) == Nothing()
```

### unwrap

```python
def unwrap(self) -> T: ...
```

Returns the contained value.

**Raises**

If `self` is a `Nothing`, raises an `UnwrapError`.

**Examples**

```python
from bento import Nothing, Option, Some

x = Some("value")
assert x.unwrap() == "value"

y: Option[str] = Nothing()
y.unwrap() # raises an UnwrapError
```

### unwrap_or

```python
def unwrap_or(self, default: T) -> T: ...
```

Returns the contained value if `self` is a `Some`, otherwise returns `default`.

Arguments passed to `unwrap_or` are eagerly evaluated. If you are passing the product of a function, we recommend using [`unwrap_or_else`](#unwrap_or_else) which is lazily evaluated.

**Examples**

```python
from bento import Nothing, Some

assert Some("foo").unwrap_or("bar") == "foo"
assert Nothing().unwrap_or("bar") == "bar"
```

### unwrap_or_else

```python
def unwrap_or_else(self, f: Callable[[], T]) -> T: ...
```

Returns the contained value if `self` is a `Some`, otherwise returns the `f` product.

**Examples**

```python
from bento import Nothing, Some

k = 10

assert Some(4).unwrap_or_else(lambda: k * 2) == 4
assert Nothing().unwrap_or_else(lambda: k * 2) == 20
```
