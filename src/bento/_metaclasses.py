from abc import ABCMeta
from typing import Any, ClassVar, override


# ==========================================
# ===            Lifetimes               ===
# ==========================================
class SingletonMeta(ABCMeta):
    _instances: ClassVar[dict[type, Any]] = {}

    @override
    def __call__(cls, *args: Any, **kwargs: Any) -> Any:
        if instance := cls._instances.get(cls):
            return instance
        instance = super().__call__(*args, **kwargs)
        cls._instances[cls] = instance
        return instance
