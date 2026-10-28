import threading
from abc import ABCMeta
from typing import Any, ClassVar, override


# ==========================================
# ===            Lifetimes               ===
# ==========================================
class _SingletonMeta(ABCMeta):
    _instances: ClassVar[dict[type[Any], Any]] = {}
    _lock: ClassVar[threading.Lock] = threading.Lock()

    @override
    def __call__[T: _SingletonMeta, **P](
        cls: type[T], *args: P.args, **kwargs: P.kwargs
    ) -> T:
        if instance := cls._instances.get(cls):
            return instance

        with cls._lock:
            if instance := cls._instances.get(cls):
                return instance

            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
            return instance

    def __clear__(cls) -> None:
        """This function is used for tests and should not be called."""
        cls._instances.clear()


class Singleton(metaclass=_SingletonMeta):
    """
    Abstract base class for all singletons.
    Inherit from this class to ensure only one instance of your class exists.
    """
