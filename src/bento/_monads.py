from abc import ABC, abstractmethod
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any, cast, final, override

from ._metaclasses import SingletonMeta

# ==========================================
# ===            Types                   ===
# ==========================================
type Option[T] = Some[T] | Nothing[T]
type Result[T, E] = Ok[T, E] | Err[E, T]


# ==========================================
# ===            Errors                  ===
# ==========================================
class UnwrapError(Exception): ...


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
        Raises an `UnwrapError` if the option is `Nothing` with a custom message provided by `msg`.
        """

    @abstractmethod
    def filter(self, predicate: Callable[[T], bool]) -> Option[T]:
        """
        Returns `Nothing` if the option is `Nothing`, otherwise calls `predicate` with the wrapped value and returns:
            - `Some(v)` if `predicate` returns `True` (where `v` is the wrapped value), and
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

    @abstractmethod
    def or_(self, optb: Option[T]) -> Option[T]:
        """Returns the option if it contains a value, otherwise returns `optb`."""

    @abstractmethod
    def or_else(self, f: Callable[[], Option[T]]) -> Option[T]:
        """Returns the option if it contains a value, otherwise calls `f` and returns the result."""

    @abstractmethod
    def unwrap(self) -> T:
        """
        Returns the contained `Some` value, consuming the `self` value.
        Raises an `UnwrapError` if the option is `Nothing`.
        """

    @abstractmethod
    def unwrap_or(self, default: T) -> T:
        """Returns the contained `Some` value or `default`."""

    @abstractmethod
    def unwrap_or_else(self, f: Callable[[], T]) -> T:
        """Returns the contained `Some` value or the result of `f`."""


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

    @override
    def or_(self, optb: Option[T]) -> Option[T]:
        return self

    @override
    def or_else(self, f: Callable[[], Option[T]]) -> Option[T]:
        return self

    @override
    def unwrap(self) -> T:
        return self.value

    @override
    def unwrap_or(self, default: T) -> T:
        return self.value

    @override
    def unwrap_or_else(self, f: Callable[[], T]) -> T:
        return self.value


@final
@dataclass(frozen=True, slots=True)
class Nothing[T = Any](_Option[T], metaclass=SingletonMeta):
    value: None = field(default=None, init=False)

    @override
    def and_[U](self, optb: Option[U]) -> Option[U]:
        return cast(Option[U], self)

    @override
    def and_then[U](self, f: Callable[[T], Option[U]]) -> Option[U]:
        return cast(Option[U], self)

    @override
    def expect(self, msg: str) -> T:
        raise UnwrapError(f"Called Option.expect() on Nothing, {msg}")

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

    @override
    def or_(self, optb: Option[T]) -> Option[T]:
        return optb

    @override
    def or_else(self, f: Callable[[], Option[T]]) -> Option[T]:
        return f()

    @override
    def unwrap(self) -> T:
        raise UnwrapError("Called Option.unwrap() on Nothing")

    @override
    def unwrap_or(self, default: T) -> T:
        return default

    @override
    def unwrap_or_else(self, f: Callable[[], T]) -> T:
        return f()


# ==========================================
# ===            Results                 ===
# ==========================================
class _Result[T, E](ABC):
    @abstractmethod
    def and_[U](self, res: Result[U, E]) -> Result[U, E]:
        """Returns `self` if the result is an `Err`, otherwise returns `res`."""

    @abstractmethod
    def and_then[U](self, f: Callable[[T], Result[U, E]]) -> Result[U, E]:
        """Returns `self` if the result is an `Err`, otherwise calls `f` with the wrapped value and returns the result."""

    @abstractmethod
    def err(self) -> Option[E]:
        """Transforms `Result[T, E]` into `Option[E]`, mapping `Err(e)` to `Some(e)` and `Ok(t)` to `Nothing`."""

    @abstractmethod
    def expect(self, msg: str) -> T:
        """
        Returns the contained `Ok` value, consuming the `self` value.
        Raises an `UnwrapError` if the result is an `Err` with a custom message provided by `msg`.
        """

    @abstractmethod
    def expect_err(self, msg: str) -> E:
        """
        Returns the contained `Err` value, consuming the `self` value.
        Raises an `UnwrapError` if the result is an `Ok` with a custom message provided by `msg`.
        """

    @abstractmethod
    def inspect(self, f: Callable[[T], Any]) -> Result[T, E]:
        """
        Calls `f` with the wrapped value if the result is an `Ok`.
        Returns the original result.
        """

    @abstractmethod
    def inspect_err(self, f: Callable[[E], Any]) -> Result[T, E]:
        """
        Calls `f` with the wrapped value if the result is an `Err`.
        Returns the original result.
        """

    @abstractmethod
    def is_err(self) -> bool:
        """Returns `True` if the result is an `Err`, otherwise returns `False`."""

    @abstractmethod
    def is_err_and(self, predicate: Callable[[E], bool]) -> bool:
        """Returns `False` if the result is an `Ok`, otherwise calls `predicate` with the wrapped value and returns the result."""

    @abstractmethod
    def is_ok(self) -> bool:
        """Returns `True` if the result is an `Ok`, otherwise returns `False`."""

    @abstractmethod
    def is_ok_and(self, predicate: Callable[[T], bool]) -> bool:
        """Returns `False` if the result is an `Err`, otherwise calls `predicate` with the wrapped value and returns the result."""

    @abstractmethod
    def map[U](self, f: Callable[[T], U]) -> Result[U, E]:
        """Maps a `Result[T, E]` to `Result[U, E]` by applying `f` to the wrapped value (if `Ok`), otherwise returns `self`."""

    @abstractmethod
    def map_err[F](self, f: Callable[[E], F]) -> Result[T, F]:
        """Maps a `Result[T, E]` to `Result[T, F]` by applying `f` to the wrapped value (if `Err`), otherwise returns `self`."""

    @abstractmethod
    def map_or[U](self, default: U, f: Callable[[T], U]) -> U:
        """Returns `default` if the result is an `Err`, otherwise calls `f` with the wrapped value and returns the result."""

    @abstractmethod
    def map_or_else[U](self, default: Callable[[E], U], f: Callable[[T], U]) -> U:
        """Returns the result of `default` with the wrapped value if the result is an `Err`, otherwise calls `f` with the wrapped value and returns the result."""

    @abstractmethod
    def ok(self) -> Option[T]:
        """Transforms `Result[T, E]` into `Option[T]`, mapping `Ok(t)` to `Some(t)` and `Err(e)` to `Nothing`."""

    @abstractmethod
    def or_[F](self, res: Result[T, F]) -> Result[T, F]:
        """Returns the result if it is an `Ok`, otherwise returns `res`."""

    @abstractmethod
    def or_else[F](self, f: Callable[[E], Result[T, F]]) -> Result[T, F]:
        """Returns the result if it is an `Ok`, otherwise calls `f` and returns the result."""

    @abstractmethod
    def unwrap(self) -> T:
        """
        Returns the contained `Ok` value, consuming the `self` value.
        Raises an `UnwrapError` if the result is an `Err`.
        """

    @abstractmethod
    def unwrap_err(self) -> E:
        """
        Returns the contained `Err` value, consuming the `self` value.
        Raises an `UnwrapError` if the result is an `Ok`.
        """

    @abstractmethod
    def unwrap_or(self, default: T) -> T:
        """Returns the contained `Ok` value or `default`."""

    @abstractmethod
    def unwrap_or_else(self, f: Callable[[E], T]) -> T:
        """Returns the contained `Ok` value or the result of `f(err)` where `err` is the contained `Err` value."""


@final
@dataclass(frozen=True, slots=True)
class Ok[T, E = Any](_Result[T, E]):
    value: T

    @override
    def and_[U](self, res: Result[U, E]) -> Result[U, E]:
        return res

    @override
    def and_then[U](self, f: Callable[[T], Result[U, E]]) -> Result[U, E]:
        return f(self.value)

    @override
    def err(self) -> Option[E]:
        return Nothing()

    @override
    def expect(self, msg: str) -> T:
        return self.value

    @override
    def expect_err(self, msg: str) -> E:
        raise UnwrapError(f"Called Result.unwrap_err() on an {self!r}, {msg}")

    @override
    def inspect(self, f: Callable[[T], Any]) -> Result[T, E]:
        f(self.value)
        return self

    @override
    def inspect_err(self, f: Callable[[E], Any]) -> Result[T, E]:
        return self

    @override
    def is_err(self) -> bool:
        return False

    @override
    def is_err_and(self, predicate: Callable[[E], bool]) -> bool:
        return False

    @override
    def is_ok(self) -> bool:
        return True

    @override
    def is_ok_and(self, predicate: Callable[[T], bool]) -> bool:
        return predicate(self.value)

    @override
    def map[U](self, f: Callable[[T], U]) -> Result[U, E]:
        return Ok(f(self.value))

    @override
    def map_err[F](self, f: Callable[[E], F]) -> Result[T, F]:
        return cast(Result[T, F], self)

    @override
    def map_or[U](self, default: U, f: Callable[[T], U]) -> U:
        return f(self.value)

    @override
    def map_or_else[U](self, default: Callable[[E], U], f: Callable[[T], U]) -> U:
        return f(self.value)

    @override
    def ok(self) -> Option[T]:
        return Some(self.value)

    @override
    def or_[F](self, res: Result[T, F]) -> Result[T, F]:
        return cast(Result[T, F], self)

    @override
    def or_else[F](self, f: Callable[[E], Result[T, F]]) -> Result[T, F]:
        return cast(Result[T, F], self)

    @override
    def unwrap(self) -> T:
        return self.value

    @override
    def unwrap_err(self) -> E:
        raise UnwrapError(f"Called Result.unwrap_err() on an {self!r}")

    @override
    def unwrap_or(self, default: T) -> T:
        return self.value

    @override
    def unwrap_or_else(self, f: Callable[[E], T]) -> T:
        return self.value


@final
@dataclass(frozen=True, slots=True)
class Err[E, T = Any](_Result[T, E]):
    value: E

    @override
    def and_[U](self, res: Result[U, E]) -> Result[U, E]:
        return cast(Result[U, E], self)

    @override
    def and_then[U](self, f: Callable[[T], Result[U, E]]) -> Result[U, E]:
        return cast(Result[U, E], self)

    @override
    def err(self) -> Option[E]:
        return Some(self.value)

    @override
    def expect(self, msg: str) -> T:
        raise UnwrapError(f"Called Result.expect() on an {self!r}, {msg}")

    @override
    def expect_err(self, msg: str) -> E:
        return self.value

    @override
    def inspect(self, f: Callable[[T], Any]) -> Result[T, E]:
        return self

    @override
    def inspect_err(self, f: Callable[[E], Any]) -> Result[T, E]:
        f(self.value)
        return self

    @override
    def is_err(self) -> bool:
        return True

    @override
    def is_err_and(self, predicate: Callable[[E], bool]) -> bool:
        return predicate(self.value)

    @override
    def is_ok(self) -> bool:
        return False

    @override
    def is_ok_and(self, predicate: Callable[[T], bool]) -> bool:
        return False

    @override
    def map[U](self, f: Callable[[T], U]) -> Result[U, E]:
        return cast(Result[U, E], self)

    @override
    def map_err[F](self, f: Callable[[E], F]) -> Result[T, F]:
        return Err(f(self.value))

    @override
    def map_or[U](self, default: U, f: Callable[[T], U]) -> U:
        return default

    @override
    def map_or_else[U](self, default: Callable[[E], U], f: Callable[[T], U]) -> U:
        return default(self.value)

    @override
    def ok(self) -> Option[T]:
        return Nothing()

    @override
    def or_[F](self, res: Result[T, F]) -> Result[T, F]:
        return res

    @override
    def or_else[F](self, f: Callable[[E], Result[T, F]]) -> Result[T, F]:
        return f(self.value)

    @override
    def unwrap(self) -> T:
        raise UnwrapError(f"Called Result.unwrap() on an {self!r}")

    @override
    def unwrap_err(self) -> E:
        return self.value

    @override
    def unwrap_or(self, default: T) -> T:
        return default

    @override
    def unwrap_or_else(self, f: Callable[[E], T]) -> T:
        return f(self.value)
