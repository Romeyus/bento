from collections.abc import Callable, Iterator, Mapping
from types import MappingProxyType
from typing import override

from bento._monads import Nothing, Option, Some


# ==========================================
# ===            Maps                    ===
# ==========================================
class Map[K, V]:
    def __init__(self, mapping: Mapping[K, V] | None = None) -> None:
        if mapping is None:
            mapping = {}
        self._inner = MappingProxyType(dict(mapping))

    def get(self, key: K) -> Option[V]:
        return Some(self._inner[key]) if key in self._inner else Nothing()

    def get_or(self, default: V, key: K) -> V:
        return self.get(key).unwrap_or(default)

    def get_or_else(self, f: Callable[[], V], key: K) -> V:
        return self.get(key).unwrap_or_else(f)

    def __contains__(self, key: K) -> bool:
        return key in self._inner

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
