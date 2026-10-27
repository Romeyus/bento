from collections.abc import Mapping
from types import MappingProxyType
from typing import override


class Map[K, V]:
    def __init__(self, mapping: Mapping[K, V] | None = None) -> None:
        if mapping is None:
            mapping = {}
        self._inner = MappingProxyType(dict(mapping))


class MutMap[K, V](Map[K, V]):
    @override
    def __init__(self, mapping: Mapping[K, V] | None = None) -> None:
        if mapping is None:
            mapping = {}
        self._inner = dict(mapping)
