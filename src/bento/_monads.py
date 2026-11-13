from abc import ABC, abstractmethod
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any, cast, final, override


# ==========================================
# ===            Errors                  ===
# ==========================================
class UnwrapError(Exception):
    """
    An `Exception` which is raised when attempting to
    unwrap a contained value that does not exist.
    """


# ==========================================
# ===            Options                 ===
# ==========================================
type Option[T] = Some[T] | Nothing[T]


class _Option[T](ABC):
    @abstractmethod
    def and_[U](self, optb: Option[U]) -> Option[U]:
        """Returns `optb` if `self` is a `Some`, otherwise returns `self`."""

    @abstractmethod
    def and_then[U](self, f: Callable[[T], Option[U]]) -> Option[U]:
        """Returns the `f` product if `self` is a `Some`, otherwise returns `self`."""

    @abstractmethod
    def expect(self, msg: str) -> T:
        """
        Returns the contained value if `self` is a `Some`,
        otherwise raises an `UnwrapError` with a custom `msg`.
        """

    @abstractmethod
    def filter(self, predicate: Callable[[T], bool]) -> Option[T]:
        """
        Returns `self` if `self` is a `Nothing`, otherwise returns:
            - `self` if the `predicate` product is `True`, or
            - a `Nothing` if the `predicate` product is `False`
        """

    @abstractmethod
    def map[U](self, f: Callable[[T], U]) -> Option[U]:
        """
        Returns a `Some` containing the `f` product if `self` is a `Some`,
        otherwise returns `self`.
        """

    @abstractmethod
    def map_or[U](self, default: U, f: Callable[[T], U]) -> U:
        """
        Returns the `f` product if `self` is a `Some`,
        otherwise returns `default`.
        """

    @abstractmethod
    def map_or_else[U](self, default: Callable[[], U], f: Callable[[T], U]) -> U:
        """
        Returns the `f` product is `self` is a `Some`,
        otherwise returns the `default` product.
        """

    @abstractmethod
    def ok_or[E](self, e: E) -> Result[T, E]:
        """
        Returns an `Ok` containing `self.value` if `self` is a `Some`,
        otherwise returns an `Err` containing `e`.
        """

    @abstractmethod
    def ok_or_else[E](self, f: Callable[[], E]) -> Result[T, E]:
        """
        Returns an `Ok` containing `self.value` if `self` is a `Some`,
        otherwise returns an `Err` containing the `f` product.
        """

    @abstractmethod
    def or_(self, optb: Option[T]) -> Option[T]:
        """Returns `optb` is `self` is a `Nothing`, otherwise returns `self`."""

    @abstractmethod
    def or_else(self, f: Callable[[], Option[T]]) -> Option[T]:
        """
        Returns the `f` product if `self` is a `Nothing`,
        otherwise returns `self`.
        """

    @abstractmethod
    def unwrap(self) -> T:
        """
        Returns the contained value if `self` is a `Some`,
        otherwise raises an `UnwrapError`.
        """

    @abstractmethod
    def unwrap_or(self, default: T) -> T:
        """
        Returns the contained value if `self` is a `Some`,
        otherwise returns `default`.
        """

    @abstractmethod
    def unwrap_or_else(self, f: Callable[[], T]) -> T:
        """
        Returns the contained value if `self` is a `Some`,
        otherwise returns the `f` product.
        """


@final
@dataclass(frozen=True, slots=True)
class Some[T](_Option[T]):
    """An `Option` monad which contains a value of type `T`."""

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
    def map[U](self, f: Callable[[T], U]) -> Option[U]:
        return Some(f(self.value))

    @override
    def map_or[U](self, default: U, f: Callable[[T], U]) -> U:
        return f(self.value)

    @override
    def map_or_else[U](self, default: Callable[[], U], f: Callable[[T], U]) -> U:
        return f(self.value)

    @override
    def ok_or[E](self, e: E) -> Result[T, E]:
        return Ok(self.value)

    @override
    def ok_or_else[E](self, f: Callable[[], E]) -> Result[T, E]:
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
class Nothing[T = Any](_Option[T]):
    """An `Option` monad which contains a value of `None`."""

    value: None = field(default=None, init=False)

    @override
    def and_[U](self, optb: Option[U]) -> Option[U]:
        return cast(Option[U], self)

    @override
    def and_then[U](self, f: Callable[[T], Option[U]]) -> Option[U]:
        return cast(Option[U], self)

    @override
    def expect(self, msg: str) -> T:
        raise UnwrapError(f"Called Option.expect() on a Nothing, {msg}")

    @override
    def filter(self, predicate: Callable[[T], bool]) -> Option[T]:
        return self

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
    def ok_or[E](self, e: E) -> Result[T, E]:
        return Err(e)

    @override
    def ok_or_else[E](self, f: Callable[[], E]) -> Result[T, E]:
        return Err(f())

    @override
    def or_(self, optb: Option[T]) -> Option[T]:
        return optb

    @override
    def or_else(self, f: Callable[[], Option[T]]) -> Option[T]:
        return f()

    @override
    def unwrap(self) -> T:
        raise UnwrapError("Called Option.unwrap() on a Nothing")

    @override
    def unwrap_or(self, default: T) -> T:
        return default

    @override
    def unwrap_or_else(self, f: Callable[[], T]) -> T:
        return f()


# ==========================================
# ===            Results                 ===
# ==========================================
type Result[T, E] = Ok[T, E] | Err[E, T]


class _Result[T, E](ABC):
    @abstractmethod
    def and_[U](self, resb: Result[U, E]) -> Result[U, E]:
        """Returns `resb` if `self` is an `Ok`, otherwise returns `self`."""

    @abstractmethod
    def and_then[U](self, f: Callable[[T], Result[U, E]]) -> Result[U, E]:
        """Returns the `f` product if `self` is an `Ok`, otherwise returns `self`."""

    @abstractmethod
    def err(self) -> Option[E]:
        """
        Returns a `Some` containing `self.value` if `self` is an `Err`,
        otherwise returns a `Nothing`.
        """

    @abstractmethod
    def expect(self, msg: str) -> T:
        """
        Returns the contained value if `self` is an `Ok`,
        otherwise raises an `UnwrapError` with a custom `msg`.
        """

    @abstractmethod
    def expect_err(self, msg: str) -> E:
        """
        Returns the contained value if `self` is an `Err`,
        otherwise raises an `UnwrapError` with a custom `msg`.
        """

    @abstractmethod
    def map[U](self, f: Callable[[T], U]) -> Result[U, E]:
        """
        Returns an `Ok` containing the `f` product if `self` is an `Ok`,
        otherwise returns `self`.
        """

    @abstractmethod
    def map_err[F](self, f: Callable[[E], F]) -> Result[T, F]:
        """
        Returns an `Err` containing the `f` product is `self` is an `Err`,
        otherwise returns `self`.
        """

    @abstractmethod
    def map_or[U](self, default: U, f: Callable[[T], U]) -> U:
        """Returns the `f` product is `self` is an `Ok`, otherwise returns `default`."""

    @abstractmethod
    def map_or_else[U](self, default: Callable[[E], U], f: Callable[[T], U]) -> U:
        """
        Returns the `f` product if `self` is an `Ok`,
        otherwise returns the `default` product.
        """

    @abstractmethod
    def ok(self) -> Option[T]:
        """
        Returns a `Some` containing `self.value` if `self` is an `Ok`,
        otherwise returns a `Nothing`.
        """

    @abstractmethod
    def or_[F](self, resb: Result[T, F]) -> Result[T, F]:
        """Returns `resb` is `self` is an `Err`, otherwise returns `self`."""

    @abstractmethod
    def or_else[F](self, f: Callable[[E], Result[T, F]]) -> Result[T, F]:
        """Returns the `f` product if `self` is an `Err`, otherwise returns `self`."""

    @abstractmethod
    def unwrap(self) -> T:
        """
        Returns the contained value if `self` is an `Ok`,
        otherwise raises an `UnwrapError`.
        """

    @abstractmethod
    def unwrap_err(self) -> E:
        """
        Returns the contained value if `self` is an `Err`,
        otherwise raises an `UnwrapError`.
        """

    @abstractmethod
    def unwrap_or(self, default: T) -> T:
        """
        Returns the contained value if `self` is an `Ok`,
        otherwise returns `default`.
        """

    @abstractmethod
    def unwrap_or_else(self, f: Callable[[E], T]) -> T:
        """
        Returns the contained value if `self` is an `Ok`,
        otherwise returns the `f` product.
        """


@final
@dataclass(frozen=True, slots=True)
class Ok[T, E = Any](_Result[T, E]):
    """A `Result` monad which contains a value of type `T`."""

    value: T

    @override
    def and_[U](self, resb: Result[U, E]) -> Result[U, E]:
        return resb

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
        raise UnwrapError(f"Called Result.expect_err() on an Ok, {msg}, {self.value!r}")

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
    def or_[F](self, resb: Result[T, F]) -> Result[T, F]:
        return cast(Result[T, F], self)

    @override
    def or_else[F](self, f: Callable[[E], Result[T, F]]) -> Result[T, F]:
        return cast(Result[T, F], self)

    @override
    def unwrap(self) -> T:
        return self.value

    @override
    def unwrap_err(self) -> E:
        raise UnwrapError(f"Called Result.unwrap_err() on an Ok, {self.value!r}")

    @override
    def unwrap_or(self, default: T) -> T:
        return self.value

    @override
    def unwrap_or_else(self, f: Callable[[E], T]) -> T:
        return self.value


@final
@dataclass(frozen=True, slots=True)
class Err[E, T = Any](_Result[T, E]):
    """A `Result` monad which contains a value of type `E`."""

    value: E

    @override
    def and_[U](self, resb: Result[U, E]) -> Result[U, E]:
        return cast(Result[U, E], self)

    @override
    def and_then[U](self, f: Callable[[T], Result[U, E]]) -> Result[U, E]:
        return cast(Result[U, E], self)

    @override
    def err(self) -> Option[E]:
        return Some(self.value)

    @override
    def expect(self, msg: str) -> T:
        raise UnwrapError(f"Called Result.expect() on an Err, {msg}, {self.value!r}")

    @override
    def expect_err(self, msg: str) -> E:
        return self.value

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
    def or_[F](self, resb: Result[T, F]) -> Result[T, F]:
        return resb

    @override
    def or_else[F](self, f: Callable[[E], Result[T, F]]) -> Result[T, F]:
        return f(self.value)

    @override
    def unwrap(self) -> T:
        raise UnwrapError(f"Called Result.unwrap() on an Err, {self.value!r}")

    @override
    def unwrap_err(self) -> E:
        return self.value

    @override
    def unwrap_or(self, default: T) -> T:
        return default

    @override
    def unwrap_or_else(self, f: Callable[[E], T]) -> T:
        return f(self.value)
