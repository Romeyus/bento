from collections.abc import (
    Callable,
    ItemsView,
    Iterable,
    Iterator,
    KeysView,
    Mapping,
    ValuesView,
)
from types import MappingProxyType
from typing import Self, override

from ._monads import Nothing, Option, Some


# ==========================================
# ===            Maps                    ===
# ==========================================
class Map[K, V]:
    def __init__(self, mapping: Mapping[K, V] | None = None) -> None:
        if mapping is None:
            mapping = {}
        self._inner = MappingProxyType(dict(mapping))

    def copy(self) -> Self:
        """Returns a shallow copy of `self`."""
        return type(self)(self._inner)

    def get(self, key: K) -> Option[V]:
        """
        Returns:
            - `Some(v)` if `key` in `self` (where `v` is the value corresponding to `key`), or
            - `Nothing` if `key` not in `self`
        """
        return Some(self._inner[key]) if key in self else Nothing()

    def get_or(self, default: V, key: K) -> V:
        """Returns `default` if `key` not in `self`, otherwise returns the value corresponding to `key`."""
        return self.get(key).unwrap_or(default)

    def get_or_else(self, f: Callable[[], V], key: K) -> V:
        """Returns the result of `f` if `key` not in `self`, otherwise returns the value corresponding to `key`."""
        return self.get(key).unwrap_or_else(f)

    def items(self) -> ItemsView[K, V]:
        return self._inner.items()

    def keys(self) -> KeysView[K]:
        return self._inner.keys()

    def values(self) -> ValuesView[V]:
        return self._inner.values()

    def __contains__(self, key: K) -> bool:
        return key in self._inner

    def __eq__(self, value: object, /) -> bool:
        if not isinstance(value, Map):
            return NotImplemented
        return self.items() == value.items()

    def __iter__(self) -> Iterator[K]:
        return iter(self._inner)

    def __len__(self) -> int:
        return len(self._inner)


class MutMap[K, V](Map[K, V]):
    @override
    def __init__(self, mapping: Mapping[K, V] | None = None) -> None:
        if mapping is None:
            mapping = {}
        self._inner = dict(mapping)

    def get_or_set(self, default: V, key: K) -> V:
        """
        Sets `default` corresponding to `key` if `key` not in `self`, then returns:
            - `Some(v)` if `key` in `self` (where `v` is the value corresponding to `key`), or
            - `Nothing` if `key` not in `self`
        """
        match self.get(key):
            case Some(value):
                return value
            case Nothing():
                self[key] = default
                return default

    def get_or_else_set(self, f: Callable[[], V], key: K) -> V:
        """
        Sets the result of `f` corresponding to `key` if `key` not in `self`, then returns:
            - `Some(v)` if `key` in `self` (where `v` is the value corresponding to `key`), or
            - `Nothing` if `key` not in `self`
        """
        match self.get(key):
            case Some(value):
                return value
            case Nothing():
                default = f()
                self[key] = default
                return default

    def pop(self, key: K) -> Option[V]:
        """
        Removes `key` if `key` in `self`, then returns:
            - `Some(v)` if `key` in `self` (where `v` was the value corresponding to `key`), or
            - `Nothing` if `key` not in `self`
        """
        return Some(self._inner.pop(key)) if key in self else Nothing()

    def pop_or(self, default: V, key: K) -> V:
        """
        Removes `key` if `key` in `self`, then returns:
            - `v` if `key` in `self` (where `v` was the value corresponding to `key`), or
            - `default` if `key` not in `self`
        """
        return self.pop(key).unwrap_or(default)

    def pop_or_else(self, f: Callable[[], V], key: K) -> V:
        """
        Removes `key` if `key` in `self`, then returns:
            - `v` if `key` in `self` (where `v` was the value corresponding to `key`), or
            - the result of `f` if `key` not in `self`
        """
        return self.pop(key).unwrap_or_else(f)

    def __setitem__(self, key: K, value: V) -> None:
        self._inner[key] = value


# ==========================================
# ===            Vectors                 ===
# ==========================================
class Vec[T]:
    def __init__(self, iterable: Iterable[T] | None = None) -> None:
        if iterable is None:
            iterable = []
        self._inner = tuple(iterable)

    def copy(self) -> Self:
        """Returns a shallow copy of `self`."""
        return type(self)(self._inner)

    def first(self) -> Option[T]:
        """Returns `Nothing` if `self` is empty, otherwise returns the first value in `self`."""
        return self.get(0)

    def get(self, index: int) -> Option[T]:
        """
        Returns:
            - `Some(v)` if `index` is in range (where `v` is the value at `index`), or
            - `Nothing` if `index` is out of range
        """
        try:
            return Some(self._inner[index])
        except IndexError:
            return Nothing()

    def get_or(self, default: T, index: int) -> T:
        """Returns `default` if `index` is out of range, otherwise returns the value at `index`."""
        return self.get(index).unwrap_or(default)

    def get_or_else(self, f: Callable[[], T], index: int) -> T:
        """Returns the result of `f` if `index` is out of range, otherwise returns the value at `index`."""
        return self.get(index).unwrap_or_else(f)

    def last(self) -> Option[T]:
        """Returns `Nothing` if `self` is empty, otherwise returns the last value in `self`."""
        return self.get(-1)

    def __contains__(self, value: T) -> bool:
        return value in self._inner

    def __eq__(self, value: object, /) -> bool:
        if not isinstance(value, Vec):
            return NotImplemented
        return tuple(self) == tuple(value)  # type: ignore

    def __iter__(self) -> Iterator[T]:
        return iter(self._inner)

    def __len__(self) -> int:
        return len(self._inner)


class MutVec[T](Vec[T]):
    @override
    def __init__(self, iterable: Iterable[T] | None = None) -> None:
        if iterable is None:
            iterable = []
        self._inner = list(iterable)

    def append(self, value: T) -> None:
        """Inserts `value` at the end of `self`."""
        self._inner.append(value)

    def clear(self) -> None:
        """Removes all values from `self`."""
        self._inner.clear()

    def extend(self, iterable: Iterable[T]) -> None:
        """Inserts all values in `iterable` at the end of `self` in the order they appear in `iterable`."""
        self._inner.extend(iterable)

    def insert(self, index: int, value: T) -> None:
        """Inserts `value` before `index`."""
        self._inner.insert(index, value)

    def pop(self, index: int = -1) -> Option[T]:
        """
        Removes the value at `index` if `index` is in range, then returns:
            - `Some(v)` if `index` is in range (where `v` is the value at `index`), or
            - `Nothing` if `index` is out of range
        """
        try:
            return Some(self._inner.pop(index))
        except IndexError:
            return Nothing()

    def pop_or(self, default: T, index: int = -1) -> T:
        """
        Removes the value at `index` if `index` is in range, then returns:
            - `v` if `index` is in range (where `v` is the value at `index`), or
            - `default` if `index` is out of range
        """
        return self.pop(index).unwrap_or(default)

    def pop_or_else(self, f: Callable[[], T], index: int = -1) -> T:
        """
        Removes the value at `index` if `index` is in range, then returns:
            - `v` if `index` is in range (where `v` is the value at `index`), or
            - the result of `f` if `index` is out of range
        """
        return self.pop(index).unwrap_or_else(f)

    def prepend(self, value: T) -> None:
        """Inserts `value` at start of `self`."""
        self._inner.insert(0, value)

    def __setitem__(self, index: int, value: T) -> None:
        self._inner[index] = value
