from abc import ABC
from typing import Any, final

# ==========================================
# ===            Types                   ===
# ==========================================
type Option[T] = Some[T] | Nothing[T]
type Result[T, E] = Ok[T, E] | Err[E, T]


# ==========================================
# ===            Options                 ===
# ==========================================
class _Option[T](ABC): ...


@final
class Some[T](_Option[T]):
    def __init__(self, value: T) -> None:
        self._value = value


@final
class Nothing[T = Any](_Option[T]): ...


# ==========================================
# ===            Results                 ===
# ==========================================
class _Result[T, E](ABC): ...


@final
class Ok[T, E = Any](_Result[T, E]):
    def __init__(self, value: T) -> None:
        self._value = value


@final
class Err[E, T = Any](_Result[T, E]):
    def __init__(self, error: E) -> None:
        self._error = error
