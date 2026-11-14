from collections.abc import (
    Callable,
    ItemsView,
    Iterable,
    Iterator,
    KeysView,
    Mapping,
    ValuesView,
)
from typing import override

from ._monads import Nothing, Option, Some


# ==========================================
# ===            Maps                    ===
# ==========================================
class Map[K, V]:
    """An immutable datastructure for key-value lookups."""

    def __init__(self, data: Mapping[K, V] | None = None) -> None:
        if data is None:
            data = {}
        self._inner = frozendict(data)  # type: ignore

    def __contains__(self, key: K) -> bool:
        return key in self._inner

    def __eq__(self, value: object, /) -> bool:
        if not isinstance(value, Map):
            return NotImplemented
        return self.items() == value.items()

    def __getitem__(self, key: K) -> V:
        return self._inner[key]

    def __iter__(self) -> Iterator[K]:
        return iter(self._inner)

    def __len__(self) -> int:
        return len(self._inner)

    def get(self, key: K) -> Option[V]:
        """
        Returns:
            - `Some(t)` if `key` is in `self` (where `t` is the corresponding value), or
            - `Nothing()` if `key` is not in `self`
        """
        return Some(self[key]) if key in self else Nothing()

    def get_or(self, default: V, key: K) -> V:
        """Helper method: equivalent to writing `self.get(key).unwrap_or(default)`."""
        return self.get(key).unwrap_or(default)

    def get_or_else(self, f: Callable[[], V], key: K) -> V:
        """Helper method: equivalent to writing `self.get(key).unwrap_or_else(f)`."""
        return self.get(key).unwrap_or_else(f)

    def items(self) -> ItemsView[K, V]:
        return self._inner.items()

    def keys(self) -> KeysView[K]:
        return self._inner.keys()

    def values(self) -> ValuesView[V]:
        return self._inner.values()


class MutMap[K, V](Map[K, V]):
    """A mutable datastructure for key-value lookups."""

    @override
    def __init__(self, data: Mapping[K, V] | None = None) -> None:
        if data is None:
            data = {}
        self._inner = dict(data)

    def __setitem__(self, key: K, value: V) -> None:
        self._inner[key] = value

    def get_or_set(self, default: V, key: K) -> V:
        """
        Returns the corresponding value if `key` is in `self`,
        otherwise sets the value at `key` to `default` and returns it.
        """
        return self._inner.setdefault(key, default)

    def get_or_else_set(self, f: Callable[[], V], key: K) -> V:
        """
        Returns the corresponding value if `key` is in `self`,
        otherwise sets the value at `key` to the `f` product and returns it.
        """
        match self.get(key):
            case Some(value):
                return value
            case Nothing():
                return self.get_or_set(f(), key)


# ==========================================
# ===            Vectors                 ===
# ==========================================
class Vec[T]:
    """An immutable datastructure for a sequence of values."""

    def __init__(self, data: Iterable[T] | None = None) -> None:
        if data is None:
            data = ()
        self._inner = tuple(data)

    def __contains__(self, value: T) -> bool:
        return value in self._inner

    def __eq__(self, value: object, /) -> bool:
        if not isinstance(value, Vec):
            return NotImplemented
        return tuple(iter(self)) == tuple(iter(value))  # type: ignore

    def __getitem__(self, idx: int) -> T:
        return self._inner[idx]

    def __iter__(self) -> Iterator[T]:
        return iter(self._inner)

    def __len__(self) -> int:
        return len(self._inner)

    def first(self) -> Option[T]:
        """
        Returns a `Some` containing the first value if `self` is not empty,
        otherwise returns a `Nothing`.
        """
        return self.get(0)

    def get(self, idx: int) -> Option[T]:
        """
        Returns:
            - `Some(t)` if `idx` is in range (where `t` is the corresponding value), or
            - `Nothing()` if `idx` is out of range
        """
        try:
            return Some(self[idx])
        except IndexError:
            return Nothing()

    def get_or(self, default: T, idx: int) -> T:
        """Helper method: equivalent to writing `self.get(idx).unwrap_or(default)`."""
        return self.get(idx).unwrap_or(default)

    def get_or_else(self, f: Callable[[], T], idx: int) -> T:
        """Helper method: equivalent to writing `self.get(idx).unwrap_or_else(f)`."""
        return self.get(idx).unwrap_or_else(f)

    def last(self) -> Option[T]:
        """
        Returns a `Some` containing the last value if `self` is not empty,
        otherwise returns a `Nothing`.
        """
        return self.get(-1)


class MutVec[T](Vec[T]):
    """A mutable datastructure for a sequence of values."""

    @override
    def __init__(self, data: Iterable[T] | None = None) -> None:
        if data is None:
            data = []
        self._inner = list(data)

    def __setitem__(self, idx: int, value: T) -> None:
        self._inner[idx] = value

    def append(self, value: T) -> None:
        """Inserts `value` at the end of `self`."""
        self._inner.append(value)

    def insert(self, idx: int, value: T) -> None:
        """Inserts `value` into `self` before `idx`."""
        self._inner.insert(idx, value)

    def pop(self, idx: int = -1) -> Option[T]:
        """
        Returns a `Nothing` if `idx` is out of range,
        otherwise removes the value at `idx` and returns a `Some` containing the value.
        """
        try:
            return Some(self._inner.pop(idx))
        except IndexError:
            return Nothing()

    def pop_or(self, default: T, idx: int = -1) -> T:
        """Helper method: equivalent to writing `self.pop(idx).unwrap_or(default)`."""
        return self.pop(idx).unwrap_or(default)

    def pop_or_else(self, f: Callable[[], T], idx: int = -1) -> T:
        """Helper method: equivalent to writing `self.pop(idx).unwrap_or_else(f)`."""
        return self.pop(idx).unwrap_or_else(f)

    def prepend(self, value: T) -> None:
        """Inserts `value` at the start of `self`."""
        self.insert(0, value)
