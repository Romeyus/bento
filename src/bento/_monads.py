from abc import ABC, abstractmethod
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any, cast, final, override

# ==========================================
# ===            Types                   ===
# ==========================================
type Option[T] = Some[T] | Nothing[T]
type Result[T, E] = Ok[T, E] | Err[E, T]


# ==========================================
# ===            Options                 ===
# ==========================================
class _Option[T](ABC):
    @abstractmethod
    def and_[U](self, optb: Option[U]) -> Option[U]:
        """Returns `Nothing` if the option is `Nothing`, otherwise returns `optb`."""

    @abstractmethod
    def and_then[U](self, f: Callable[[T], Option[U]]) -> Option[U]:
        """Returns `Nothing` if the option is `Nothing`, otherwise calls `f` with the wrapped value and returns the result."""


@final
@dataclass(frozen=True, slots=True)
class Some[T](_Option[T]):
    value: T

    @override
    def and_[U](self, optb: Option[U]) -> Option[U]:
        return optb

    @override
    def and_then[U](self, f: Callable[[T], Option[U]]) -> Option[U]:
        return f(self.value)


@final
@dataclass(frozen=True, slots=True)
class Nothing[T = Any](_Option[T]):
    value: None = field(default=None, init=False)

    @override
    def and_[U](self, optb: Option[U]) -> Option[U]:
        return cast(Option[U], self)

    @override
    def and_then[U](self, f: Callable[[T], Option[U]]) -> Option[U]:
        return cast(Option[U], self)


# ==========================================
# ===            Results                 ===
# ==========================================
class _Result[T, E](ABC): ...


@final
@dataclass(frozen=True, slots=True)
class Ok[T, E = Any](_Result[T, E]):
    value: T


@final
@dataclass(frozen=True, slots=True)
class Err[E, T = Any](_Result[T, E]):
    value: E
