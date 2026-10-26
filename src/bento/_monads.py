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

    @abstractmethod
    def map[U](self, f: Callable[[T], U]) -> Option[U]:
        """Maps an `Option[T]` to `Option[U]` by applying `f` to the wrapped value (if `Some`), otherwise returns `Nothing`."""

    @abstractmethod
    def map_or[U](self, default: U, f: Callable[[T], U]) -> U:
        """Returns `default` if the option is `Nothing`, otherwise calls `f` with the wrapped value and returns the result."""

    @abstractmethod
    def map_or_else[U](self, default: Callable[[], U], f: Callable[[T], U]) -> U:
        """Returns the result of `default` if the option is `Nothing`, otherwise calls `f` with the wrapped value and returns the result."""

    @abstractmethod
    def ok_or[E](self, err: E) -> Result[T, E]:
        """Transforms `Option[T]` into `Result[T, E]`, mapping `Some(v)` to `Ok(v)` and `Nothing` to `Err(err)`."""

    @abstractmethod
    def ok_or_else[E](self, err: Callable[[], E]) -> Result[T, E]:
        """Transforms `Option[T]` into `Result[T, E]`, mapping `Some(v)` to `Ok(v)` and `Nothing` to `Err(err())`."""


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

    @override
    def map[U](self, f: Callable[[T], U]) -> Option[U]:
        return Some(f(self.value))

    @override
    def map_or[U](self, default: U, f: Callable[[T], U]) -> U:
        return f(self.value)

    @override
    def map_or_else[U](self, default: Callable[[], U], f: Callable[[T], U]) -> U:
        return f(self.value)

    @override
    def ok_or[E](self, err: E) -> Result[T, E]:
        return Ok(self.value)

    @override
    def ok_or_else[E](self, err: Callable[[], E]) -> Result[T, E]:
        return Ok(self.value)


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

    @override
    def map[U](self, f: Callable[[T], U]) -> Option[U]:
        return cast(Option[U], self)

    @override
    def map_or[U](self, default: U, f: Callable[[T], U]) -> U:
        return default

    @override
    def map_or_else[U](self, default: Callable[[], U], f: Callable[[T], U]) -> U:
        return default()

    @override
    def ok_or[E](self, err: E) -> Result[T, E]:
        return Err(err)

    @override
    def ok_or_else[E](self, err: Callable[[], E]) -> Result[T, E]:
        return Err(err())


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
