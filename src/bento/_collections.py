from collections.abc import Callable, ItemsView, Iterator, KeysView, Mapping, ValuesView
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
        return Some(self._inner[key]) if key in self._inner else Nothing()

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
        try:
            return Some(self._inner.pop(key))
        except KeyError:
            return Nothing()

    def pop_or(self, default: V, key: K) -> V:
        return self.pop(key).unwrap_or(default)

    def pop_or_else(self, f: Callable[[], V], key: K) -> V:
        return self.pop(key).unwrap_or_else(f)

    def __setitem__(self, key: K, value: V) -> None:
        self._inner[key] = value
