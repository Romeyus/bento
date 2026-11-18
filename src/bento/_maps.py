from collections.abc import (
    Callable,
    ItemsView,
    Iterator,
    KeysView,
    Mapping,
    ValuesView,
)
from typing import override

from ._monads import Nothing, Option, Some


class Map[K, V]:
    """An immutable datastructure for key-value lookups."""

    def __init__(self, data: Mapping[K, V] | None = None) -> None:
        if data is None:
            data = {}
        self._inner = frozendict(data)  # type: ignore

    def __contains__(self, key: K) -> bool:
        """Returns `True` if `key` is in `self`, otherwise returns `False`."""
        return key in self._inner

    def __eq__(self, value: object, /) -> bool:
        """
        Returns `True` if `value` is equal to `self`, otherwise returns `False`.

        This checks for equality between `items()`.
        """
        if not isinstance(value, Map):
            return NotImplemented
        return self.items() == value.items()

    def __getitem__(self, key: K) -> V:
        """
        Gets the value corresponding to `key` if `key` is in `self`,
        otherwise raises a `KeyError`.
        """
        return self._inner[key]

    def __iter__(self) -> Iterator[K]:
        """Returns an iterator of the contained keys."""
        return iter(self._inner)

    def __len__(self) -> int:
        """Returns the length of `self` by counting the number of keys."""
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
        """Returns a sequence of key-value tuple pairs."""
        return self._inner.items()

    def keys(self) -> KeysView[K]:
        """Returns a sequence of keys."""
        return self._inner.keys()

    def values(self) -> ValuesView[V]:
        """Returns a sequence of values."""
        return self._inner.values()


class MutMap[K, V](Map[K, V]):
    """A mutable datastructure for key-value lookups."""

    @override
    def __init__(self, data: Mapping[K, V] | None = None) -> None:
        if data is None:
            data = {}
        self._inner = dict(data)

    def __setitem__(self, key: K, value: V) -> None:
        """Sets the value corresponding to `key` to `value`."""
        self._inner[key] = value

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

    def get_or_set(self, default: V, key: K) -> V:
        """
        Returns the corresponding value if `key` is in `self`,
        otherwise sets the value at `key` to `default` and returns it.
        """
        return self._inner.setdefault(key, default)
