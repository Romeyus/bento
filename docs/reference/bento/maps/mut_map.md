# MutMap

```python
class MutMap[K, V](Map[K, V]):
    def __init__(self, data: Mapping[K, V] | None = None) -> None: ...
```

A `MutMap` is a mutable datastructure for key-value lookups and mutations. It inherits all methods from [`Map`](./map) and has some additional methods for mutating its own data.

## Methods

### \_\_setitem\_\_

```python
def __setitem__(self, key: K, value: V) -> None: ...
```

Sets the value corresponding to `key` to `value`.

**Examples**

```python
from bento import MutMap

map = MutMap({"a": 1, "b": 2, "c": 3})

map["b"] = 200
assert map["b"] == 200

map["z"] = 26
assert map["z"] == 26
```

### get_or_else_set

```python
def get_or_else_set(self, f: Callable[[], V], key: K) -> V: ...
```

Returns the corresponding value if `key` is in `self`, otherwise sets the value at `key` to the `f` product and returns it.

**Examples**

```python
from bento import MutMap

map = MutMap({"a": 1, "b": 2, "c": 3})

assert map.get_or_else_set(lambda: 100, "a") == 1
assert map.get_or_else_set(lambda: 100, "z") == 100
```

### get_or_set

```python
def get_or_set(self, default: V, key: K) -> V: ...
```

Returns the corresponding value if `key` is in `self`, otherwise sets the value at `key` to `default` and returns it.

Arguments passed to `get_or_set` are eagerly evaluated. If you are passing the product of a function, we recommend using [`get_or_else_set`](#get_or_else_set) which is lazily evaluated.

**Examples**

```python
from bento import MutMap

map = MutMap({"a": 1, "b": 2, "c": 3})

assert map.get_or_set(100, "a") == 1
assert map.get_or_set(100, "z") == 100
```
