from abc import ABC, abstractmethod
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any, cast, final, override

from bento._exceptions import Panic

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

    @abstractmethod
    def expect(self, msg: str) -> T:
        """
        Returns the contained `Some` value, consuming the `self` value.
        Raises a `Panic` exception if the option is `Nothing` with a custom message provided by `msg`.
        """

    @abstractmethod
    def filter(self, predicate: Callable[[T], bool]) -> Option[T]:
        """
        Returns `Nothing` if the option is `Nothing`, otherwise calls `predicate` with the wrapped value and returns:
            - `Some[T]` if `predicate` returns `True` (where `T` is the wrapped value), and
            - `Nothing` if `predicate` returns `False`
        """

    @abstractmethod
    def inspect(self, f: Callable[[T], Any]) -> Option[T]:
        """
        Calls `f` with the wrapped value if the option is `Some`.
        Returns the original option.
        """

    @abstractmethod
    def is_nothing(self) -> bool:
        """Returns `True` if the option is `Nothing`, otherwise returns `False`."""

    @abstractmethod
    def is_nothing_or(self, predicate: Callable[[T], bool]) -> bool:
        """Returns `True` if the option is `Nothing`, otherwise calls `predicate` with the wrapped value and returns the result."""

    @abstractmethod
    def is_some(self) -> bool:
        """Returns `True` if the option is a `Some`, otherwise returns `False`."""

    @abstractmethod
    def is_some_and(self, predicate: Callable[[T], bool]) -> bool:
        """Returns `True` if the option is a `Some` and the the wrapped value matches `predicate`, otherwise returns `False`."""


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

    @override
    def expect(self, msg: str) -> T:
        return self.value

    @override
    def filter(self, predicate: Callable[[T], bool]) -> Option[T]:
        return self if predicate(self.value) else Nothing()

    @override
    def inspect(self, f: Callable[[T], Any]) -> Option[T]:
        f(self.value)
        return self

    @override
    def is_nothing(self) -> bool:
        return False

    @override
    def is_nothing_or(self, predicate: Callable[[T], bool]) -> bool:
        return predicate(self.value)

    @override
    def is_some(self) -> bool:
        return True

    @override
    def is_some_and(self, predicate: Callable[[T], bool]) -> bool:
        return predicate(self.value)


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

    @override
    def expect(self, msg: str) -> T:
        raise Panic(f"Called Option.expect() on Nothing, {msg}")

    @override
    def filter(self, predicate: Callable[[T], bool]) -> Option[T]:
        return self

    @override
    def inspect(self, f: Callable[[T], Any]) -> Option[T]:
        return self

    @override
    def is_nothing(self) -> bool:
        return True

    @override
    def is_nothing_or(self, predicate: Callable[[T], bool]) -> bool:
        return True

    @override
    def is_some(self) -> bool:
        return False

    @override
    def is_some_and(self, predicate: Callable[[T], bool]) -> bool:
        return False


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
