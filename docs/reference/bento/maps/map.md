# Map

```python
class Map[K, V]:
    def __init__(self, data: Mapping[K, V] | None = None) -> None: ...
```

A `Map` is an immutable datastructure for key-value lookups. Its intention is to have the same general API as `Mapping` but with a few tweaks.

## Methods

### \_\_contains\_\_

```python
def __contains__(self, key: K) -> bool: ...
```

Returns `True` if `key` is in `self`, otherwise returns `False`.

**Examples**

```python
from bento import Map

map = Map({"a": 1, "b": 2, "c": 3})

assert ("a" in map) is True
assert ("z" in map) is False
```

### \_\_eq\_\_

```python
def __eq__(self, value: object) -> bool: ...
```

Returns `True` if `value` is equal to `self`, otherwise returns `False`.

This checks for equality between [`items()`](#items).

**Examples**

```python
from bento import Map

map = Map({"a": 1, "b": 2, "c": 3})

assert (map == Map({"a": 1, "b": 2, "c": 3})) is True
assert (map == Map({"a": 1, "b": 2, "c": 42})) is False
assert (map == 2) is False
assert (map == "Hello world!") is False
```

### \_\_getitem\_\_

```python
def __getitem__(self, key: K) -> V: ...
```

Gets the value corresponding to `key`.

**Raises**

Raises a `KeyError` if `key` is not in `self`.

**Examples**

```python
from bento import Map

map = Map({"a": 1, "b": 2, "c": 3})

assert map["a"] == 1
map["z"] # raises a KeyError
```

### \_\_iter\_\_

```python
def __iter__(self) -> Iterator[K]: ...
```

Returns an iterator of the contained keys.

**Examples**

```python
from bento import Map

map = Map({"a": 1, "b": 2, "c": 3})

assert list(iter(map)) == ["a", "b", "c"]
```

### \_\_len\_\_

```python
def __len__(self) -> int: ...
```

Returns the length of `self` by counting the number of keys.

**Examples**

```python
from bento import Map

map = Map({"a": 1, "b": 2, "c": 3})

assert len(map) == 3
```

### get

```python
def get(self, key: K) -> Option[V]: ...
```

Returns:

- `Some(t)` if `key` is in `self` (where `t` is the corresponding value), or
- `Nothing()` if `key` is not in `self`

**Examples**

```python
from bento import Map, Nothing, Some

map = Map({"a": 1, "b": 2, "c": 3})

assert map.get("a") == Some(1)
assert map.get("z") == Nothing()
```

### get_or

```python
def get_or(self, default: V, key: K) -> V: ...
```

_Helper method_: equivalent to writing `self.get(key).unwrap_or(default)`.

Arguments passed to `get_or` are eagerly evaluated. If you are passing the product of a function, we recommend using [`get_or_else`](#get_or_else) which is lazily evaluated.

**Examples**

```python
from bento import Map

map = Map({"a": 1, "b": 2, "c": 3})

assert map.get_or(100, "b") == 2
assert map.get_or(100, "z") == 100
```

### get_or_else

```python
def get_or_else(self, f: Callable[[], V], key: K) -> V: ...
```

_Helper method_: equivalent to writing `self.get(key).unwrap_or_else(f)`.

**Examples**

```python
from bento import Map

map = Map({"a": 1, "b": 2, "c": 3})

assert map.get_or_else(lambda: 100, "b") == 2
assert map.get_or_else(lambda: 100, "z") == 100
```

### items

```python
def items(self) -> ItemsView[K, V]: ...
```

Returns a sequence of key-value tuple pairs.

**Examples**

```python
from bento import Map

map = Map({"a": 1, "b": 2, "c": 3})

assert list(map.items()) == [("a", 1), ("b", 2), ("c", 3)]
```

### keys

```python
def keys(self) -> KeysView[K]: ...
```

Returns a sequence of keys.

**Examples**

```python
from bento import Map

map = Map({"a": 1, "b": 2, "c": 3})

assert list(map.keys()) == ["a", "b", "c"]
```

### values

```python
def values(self) -> ValuesView[V]: ...
```

Returns a sequence of values.

**Examples**

```python
from bento import Map

map = Map({"a": 1, "b": 2, "c": 3})

assert list(map.values()) == [1, 2, 3]
```
