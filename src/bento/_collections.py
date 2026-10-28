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

from bento._monads import Nothing, Option, Some


# ==========================================
# ===            Maps                    ===
# ==========================================
class Map[K, V]:
    def __init__(self, mapping: Mapping[K, V] | None = None) -> None:
        if mapping is None:
            mapping = {}
        self._inner = MappingProxyType(dict(mapping))

    def copy(self) -> Self:
        return type(self)(self._inner)

    def get(self, key: K) -> Option[V]:
        return Some(self._inner[key]) if key in self else Nothing()

    def get_or(self, default: V, key: K) -> V:
        return self.get(key).unwrap_or(default)

    def get_or_else(self, f: Callable[[], V], key: K) -> V:
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
        match self.get(key):
            case Some(value):
                return value
            case Nothing():
                self[key] = default
                return default

    def get_or_else_set(self, f: Callable[[], V], key: K) -> V:
        match self.get(key):
            case Some(value):
                return value
            case Nothing():
                default = f()
                self[key] = default
                return default

    def pop(self, key: K) -> Option[V]:
        return Some(self._inner.pop(key)) if key in self else Nothing()

    def pop_or(self, default: V, key: K) -> V:
        return self.pop(key).unwrap_or(default)

    def pop_or_else(self, f: Callable[[], V], key: K) -> V:
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
        return type(self)(self._inner)

    def first(self) -> Option[T]:
        return self.get(0)

    def get(self, index: int) -> Option[T]:
        try:
            return Some(self._inner[index])
        except IndexError:
            return Nothing()

    def get_or(self, default: T, index: int) -> T:
        return self.get(index).unwrap_or(default)

    def get_or_else(self, f: Callable[[], T], index: int) -> T:
        return self.get(index).unwrap_or_else(f)

    def last(self) -> Option[T]:
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
        self._inner.append(value)

    def clear(self) -> None:
        self._inner.clear()

    def extend(self, iterable: Iterable[T]) -> None:
        self._inner.extend(iterable)

    def insert(self, index: int, value: T) -> None:
        self._inner.insert(index, value)

    def pop(self, index: int = -1) -> Option[T]:
        try:
            return Some(self._inner.pop(index))
        except IndexError:
            return Nothing()

    def pop_or(self, default: T, index: int = -1) -> T:
        return self.pop(index).unwrap_or(default)

    def pop_or_else(self, f: Callable[[], T], index: int = -1) -> T:
        return self.pop(index).unwrap_or_else(f)

    def prepend(self, value: T) -> None:
        self._inner.insert(0, value)

    def __setitem__(self, index: int, value: T) -> None:
        self._inner[index] = value
