# Result

```python
type Result[T, E] = Ok[T] | Err[E]
```

The `Result` type is a union of `Ok` and `Err`, where `Ok` represents the success path and `Err` represents the failure path.

## Variants

### Err

```python
class Err[E]:
    def __init__(self, value: E) -> None: ...
```

Contains a value of type `E`.

### Ok

```python
class Ok[T]:
    def __init__(self, value: T) -> None: ...
```

Contains a value of type `T`.

## Methods

### and_

```python
def and_[U](self, resb: Result[U, E]) -> Result[U, E]: ...
```

Returns `resb` if `self` is an `Ok`, otherwise returns `self`.

Arguments passed to `and_` are eagerly evaluated. If you are passing the product of a function, we recommend using [`and_then`](#and_then) which is lazily evaluated.

**Examples**

```python
from bento import Err, Ok, Result

x: Result[int, str] = Ok(2)
y: Result[str, str] = Err("late error")
assert x.and_(y) == Err("late error")

x: Result[int, str] = Err("early error")
y: Result[str, str] = Ok("foo")
assert x.and_(y) == Err("early error")

x: Result[int, str] = Err("not a 2")
y: Result[str, str] = Err("late error")
assert x.and_(y) == Err("not a 2")

x: Result[int, str] = Ok(2)
y: Result[str, str] = Ok("different result type")
assert x.and_(y) == Ok("different result type")
```

### and_then

```python
def and_then[U](self, f: Callable[[T], Result[U, E]]) -> Result[U, E]: ...
```

Returns the `f` product if `self` is an `Ok`, otherwise returns `self`.

The `f` product is the return value of `f` when called with the contained value.

**Examples**

```python
from collections.abc import Callable

from bento import Err, Ok, Result

def divide_by(denominator: int) -> Callable[[int], Result[float, str]]:
    def wrapper(numerator: int) -> Result[float, str]:
        if denominator == 0:
            return Err("cannot divide by zero")
        return Ok(numerator / denominator)

    return wrapper

assert Ok(10).and_then(divide_by(2)) == Ok(5)
assert Err("early error").and_then(divide_by(2)) == Err("early error")
assert Ok(10).and_then(divide_by(0)) == Err("cannot divide by zero")
```

### err

```python
def err(self) -> Option[E]: ...
```

Returns a `Some` containing `self.value` if `self` is an `Err`, otherwise returns a `Nothing`.

**Examples**

```python
from bento import Err, Nothing, Ok, Result, Some

x: Result[int, str] = Ok(2)
assert x.err() == Nothing()

y: Result[int, str] = Err("nothing here")
assert y.err() == Some("nothing here")
```

### expect

```python
def expect(self, msg: str) -> T: ...
```

Returns the contained value.

**Raises**

If `self` is an `Err`, raises an `UnwrapError` containing `msg`.

**Examples**

```python
from bento import Err, Ok, Result

x: Result[int, str] = Ok(2)
assert x.expect("testing expect") == 2

y: Result[int, str] = Err("some failure")
y.expect("testing expect") # raises an UnwrapError containing 'testing expect'
```

### expect_err

```python
def expect_err(self, msg: str) -> E: ...
```

Returns the contained value.

**Raises**

If `self` is an `Ok`, raises an `UnwrapError` containing `msg`.

**Examples**

```python
from bento import Err, Ok, Result

x: Result[int, str] = Ok(2)
x.expect_err("testing expect_err") # raises an UnwrapError containing 'testing expect_err'

y: Result[int, str] = Err("some failure")
assert y.expect_err("testing expect_err") == "some failure"
```

### map

```python
def map[U](self, f: Callable[[T], U]) -> Result[U, E]: ...
```

Returns an `Ok` containing the `f` product if `self` is an `Ok`, otherwise returns `self`.

**Examples**

```python
from bento import Err, Ok, Result

def sq_then_to_str(x: int) -> str:
    return str(x**2)

assert Ok(2).map(sq_then_to_str) == Ok("4")
assert Err("early error").map(sq_then_to_str) == Err("early error")
```

### map_err

```python
def map_err[F](self, f: Callable[[E], F]) -> Result[T, F]: ...
```

Returns an `Err` containing the `f` product is `self` is an `Err`, otherwise returns `self`.

**Examples**

```python
from bento import Err, Ok, Result

def stringify(x: int) -> str:
    return f"error code: {x}"

x: Result[int, int] = Ok(200)
assert x.map_err(stringify) == Ok(200)

y: Result[int, int] = Err(404)
assert y.map_err(stringify) == Err("error code: 404")
```

### map_or

```python
def map_or[U](self, default: U, f: Callable[[T], U]) -> U: ...
```

Returns the `f` product is `self` is an `Ok`, otherwise returns `default`.

Arguments passed to `map_or` are eagerly evaluated. If you are passing the product of a function, we recommend using [`map_or_else`](#map_or_else) which is lazily evaluated.

**Examples**

```python
from bento import Err, Ok, Result

x: Result[str, str] = Ok("foo")
assert x.map_or(42, len) == 3

y: Result[str, str] = Err("bar")
assert y.map_or(42, len) == 42
```

### map_or_else

```python
def map_or_else[U](self, default: Callable[[E], U], f: Callable[[T], U]) -> U: ...
```

Returns the `f` product if `self` is an `Ok`, otherwise returns the `default` product.

**Examples**

```python
from bento import Err, Ok, Result

x: Result[str, str] = Ok("foo")
assert x.map_or_else(lambda e: len(e) * 2, len) == 3

y: Result[str, str] = Err("bar")
assert y.map_or_else(lambda e: len(e) * 2, len) == 6
```

### ok

```python
def ok(self) -> Option[T]: ...
```

Returns a `Some` containing `self.value` if `self` is an `Ok`, otherwise returns a `Nothing`.

**Examples**

```python
from bento import Err, Nothing, Ok, Result, Some

x: Result[int, str] = Ok(2)
assert x.ok() == Some(2)

y: Result[int, str] = Err("nothing here")
assert y.ok() == Nothing()
```

### or_

```python
def or_[F](self, resb: Result[T, F]) -> Result[T, F]: ...
```

Returns `resb` is `self` is an `Err`, otherwise returns `self`.

Arguments passed to `or_` are eagerly evaluated. If you are passing the product of a function, we recommend using [`or_else`](#or_else) which is lazily evaluated.

```python
from bento import Err, Ok, Result

x: Result[int, str] = Ok(2)
y: Result[int, str] = Err("late error")
assert x.or_(y) == Ok(2)

x: Result[int, str] = Err("early error")
y: Result[int, str] = Ok(2)
assert x.or_(y) == Ok(2)

x: Result[int, str] = Err("not a 2")
y: Result[int, str] = Err("late error")
assert x.or_(y) == Err("late error")

x: Result[int, str] = Ok(2)
y: Result[int, str] = Ok(100)
assert x.or_(y) == Ok(2)
```

### or_else

```python
def or_else[F](self, f: Callable[[E], Result[T, F]]) -> Result[T, F]: ...
```

Returns the `f` product if `self` is an `Err`, otherwise returns `self`.

**Examples**

```python
from bento import Err, Ok, Result

def sq(x: int) -> Result[int, int]:
    return Ok(x**2)

def err(x: int) -> Result[int, int]:
    return Err(x)

assert Ok(2).or_else(sq).or_else(sq) == Ok(2)
assert Ok(2).or_else(err).or_else(sq) == Ok(2)
assert Err(3).or_else(sq).or_else(err) == Ok(9)
assert Err(3).or_else(err).or_else(err) == Err(3)
```

### unwrap

```python
def unwrap(self) -> T: ...
```

Returns the contained value.

**Raises**

If `self` is an `Err`, raises an `UnwrapError`.

**Examples**

```python
from bento import Err, Ok, Result

x: Result[int, str] = Ok(2)
assert x.unwrap() == 2

y: Result[int, str] = Err("some failure")
y.unwrap() # raises an UnwrapError
```

### unwrap_err

```python
def unwrap_err(self) -> E: ...
```

Returns the contained value.

**Raises**

If `self` is an `Ok`, raises an `UnwrapError`.

**Examples**

```python
from bento import Err, Ok, Result

x: Result[int, str] = Err("some error")
assert x.unwrap_err() == "some error"

y: Result[int, str] = Ok(2)
y.unwrap_err() # raises an UnwrapError
```

### unwrap_or

```python
def unwrap_or(self, default: T) -> T: ...
```

Returns the contained value if `self` is an `Ok`, otherwise returns `default`.

Arguments passed to `unwrap_or` are eagerly evaluated. If you are passing the product of a function, we recommend using [`unwrap_or_else`](#unwrap_or_else) which is lazily evaluated.

**Examples**

```python
from bento import Err, Ok, Result

x: Result[int, str] = Ok(9)
assert x.unwrap_or(42) == 9

y: Result[int, str] = Err("some failure")
assert y.unwrap_or(42) == 42
```

### unwrap_or_else

```python
def unwrap_or_else(self, f: Callable[[E], T]) -> T: ...
```

Returns the contained value if `self` is an `Ok`, otherwise returns the `f` product.

**Examples**

```python
from bento import Err, Ok, Result

x: Result[int, str] = Ok(2)
assert x.unwrap_or_else(len) == 2

y: Result[int, str] = Err("foo")
assert y.unwrap_or_else(len) == 3
```
