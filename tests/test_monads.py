from typing import Any
from unittest import mock

import pytest

from bento import Err, Nothing, Ok, Option, Result, Some, UnwrapError


# ==========================================
# ===            Fixtures                ===
# ==========================================
@pytest.fixture
def some() -> Option[int]:
    return Some(100)


@pytest.fixture
def nothing() -> Option[int]:
    return Nothing()


@pytest.fixture
def ok() -> Result[int, str]:
    return Ok(100)


@pytest.fixture
def err() -> Result[int, str]:
    return Err("Failure")


# ==========================================
# ===            Options                 ===
# ==========================================
class TestSome:
    # ==========and_==========
    @pytest.mark.parametrize(
        "optb",
        [
            [Some(200)],
            [Nothing()],
        ],
    )
    def test_and_should_return_optb(self, some: Option[int], optb: Option[Any]) -> None:
        assert some.and_(optb) is optb

    # ==========and_then==========
    def test_and_then_should_return_result_of_f(self, some: Option[int]) -> None:
        assert some.and_then(lambda v: Some(v * 2)) == Some(200)

    def test_and_then_should_call_f_with_wrapped_value(self, some: Option[int]) -> None:
        f = mock.Mock()
        some.and_then(f)
        f.assert_called_once_with(100)

    # ==========expect==========
    def test_expect_should_return_contained_value(self, some: Option[int]) -> None:
        assert some.expect("Testing expect") == 100

    # ==========filter==========
    def test_filter_should_return_self_if_predicate_returns_true(
        self, some: Option[int]
    ) -> None:
        assert some.filter(lambda _: True) is some

    def test_filter_should_return_nothing_if_predicate_returns_false(
        self, some: Option[int]
    ) -> None:
        assert some.filter(lambda _: False) == Nothing()

    def test_filter_should_call_predicate_with_wrapped_value(
        self, some: Option[int]
    ) -> None:
        predicate = mock.Mock()
        some.filter(predicate)
        predicate.assert_called_once_with(100)

    # ==========inspect==========
    def test_inspect_should_return_self(self, some: Option[int]) -> None:
        assert some.inspect(print) is some

    def test_inspect_should_call_f_with_wrapped_value(self, some: Option[int]) -> None:
        f = mock.Mock()
        some.inspect(f)
        f.assert_called_once_with(100)

    # ==========is_nothing==========
    def test_is_nothing_should_return_false(self, some: Option[int]) -> None:
        assert some.is_nothing() is False

    # ==========is_nothing_or==========
    @pytest.mark.parametrize(
        "result",
        [
            [True],
            [False],
        ],
    )
    def test_is_nothing_or_should_return_result_of_predicate(
        self, some: Option[int], result: bool
    ) -> None:
        assert some.is_nothing_or(lambda _: result) is result

    def test_is_nothing_or_should_call_predicate_with_wrapped_value(
        self, some: Option[int]
    ) -> None:
        predicate = mock.Mock()
        some.is_nothing_or(predicate)
        predicate.assert_called_once_with(100)

    # ==========is_some==========
    def test_is_some_should_return_true(self, some: Option[int]) -> None:
        assert some.is_some() is True

    # ==========is_some_and==========
    @pytest.mark.parametrize(
        "result",
        [
            [True],
            [False],
        ],
    )
    def test_is_some_and_should_return_result_of_predicate(
        self, some: Option[int], result: bool
    ) -> None:
        assert some.is_some_and(lambda _: result) is result

    def test_is_some_and_should_call_predicate(self, some: Option[int]) -> None:
        predicate = mock.Mock()
        some.is_some_and(predicate)
        predicate.assert_called_once_with(100)

    # ==========map==========
    def test_map_should_return_some_with_result_of_f(self, some: Option[int]) -> None:
        assert some.map(lambda v: v * 2) == Some(200)

    def test_map_should_call_f_with_wrapped_value(self, some: Option[int]) -> None:
        f = mock.Mock()
        some.map(f)
        f.assert_called_once_with(100)

    # ==========map_or==========
    def test_map_or_should_return_result_of_f(self, some: Option[int]) -> None:
        assert some.map_or(0, lambda v: v * 2) == 200

    def test_map_or_should_call_f_with_wrapped_value(self, some: Option[int]) -> None:
        f = mock.Mock()
        some.map_or(0, f)
        f.assert_called_once_with(100)

    # ==========map_or_else==========
    def test_map_or_else_should_return_result_of_f(self, some: Option[int]) -> None:
        assert some.map_or_else(lambda: 0, lambda v: v * 2) == 200

    def test_map_or_else_should_call_f_with_wrapped_value(
        self, some: Option[int]
    ) -> None:
        f = mock.Mock()
        some.map_or_else(lambda: 0, f)
        f.assert_called_once_with(100)

    def test_map_or_else_should_not_call_default(self, some: Option[int]) -> None:
        default = mock.Mock()
        some.map_or_else(default, lambda v: v * 2)
        default.assert_not_called()

    # ==========ok_or==========
    def test_ok_or_should_return_ok_with_wrapped_value(self, some: Option[int]) -> None:
        assert some.ok_or("Failure") == Ok(100)

    # ==========ok_or_else==========
    def test_ok_or_else_should_return_ok_with_wrapped_value(
        self, some: Option[int]
    ) -> None:
        assert some.ok_or_else(lambda: "Failure") == Ok(100)

    def test_ok_or_else_should_not_call_err(self, some: Option[int]) -> None:
        err = mock.Mock()
        some.ok_or_else(err)
        err.assert_not_called()

    # ==========or_==========
    @pytest.mark.parametrize(
        "optb",
        [
            [Some(200)],
            [Nothing()],
        ],
    )
    def test_or_should_return_self(self, some: Option[int], optb: Option[int]) -> None:
        assert some.or_(optb) is some

    # ==========or_else==========
    def test_or_else_should_return_self(self, some: Option[int]) -> None:
        assert some.or_else(lambda: Nothing()) is some

    def test_or_else_should_not_call_f(self, some: Option[int]) -> None:
        f = mock.Mock()
        some.or_else(f)
        f.assert_not_called()

    # ==========unwrap==========
    def test_unwrap_should_return_contained_value(self, some: Option[int]) -> None:
        assert some.unwrap() == 100

    # ==========unwrap_or==========
    def test_unwrap_or_should_return_contained_value(self, some: Option[int]) -> None:
        assert some.unwrap_or(0) == 100

    # ==========unwrap_or_else==========
    def test_unwrap_or_else_should_return_contained_value(
        self, some: Option[int]
    ) -> None:
        assert some.unwrap_or_else(lambda: 0) == 100

    def test_unwrap_or_else_should_not_call_f(self, some: Option[int]) -> None:
        f = mock.Mock()
        some.unwrap_or_else(f)
        f.assert_not_called()


class TestNothing:
    # ==========and_==========
    @pytest.mark.parametrize(
        "optb",
        [
            [Some(200)],
            [Nothing()],
        ],
    )
    def test_and_should_return_nothing(
        self, nothing: Option[int], optb: Option[Any]
    ) -> None:
        assert nothing.and_(optb) is nothing

    # ==========and_then==========
    def test_and_then_should_return_nothing(self, nothing: Option[int]) -> None:
        assert nothing.and_then(lambda v: Some(v * 2)) is nothing

    def test_and_then_should_not_call_f(self, nothing: Option[int]) -> None:
        f = mock.Mock()
        nothing.and_then(f)
        f.assert_not_called()

    # ==========expect==========
    def test_expect_should_raise_UnwrapError_with_msg(
        self, nothing: Option[int]
    ) -> None:
        with pytest.raises(UnwrapError, match="Testing expect"):
            nothing.expect("Testing expect")

    # ==========filter==========
    def test_filter_should_return_nothing(self, nothing: Option[int]) -> None:
        assert nothing.filter(lambda _: True) is nothing

    def test_filter_should_not_call_predicate(self, nothing: Option[int]) -> None:
        predicate = mock.Mock()
        nothing.filter(predicate)
        predicate.assert_not_called()

    # ==========inspect==========
    def test_inspect_should_return_nothing(self, nothing: Option[int]) -> None:
        assert nothing.inspect(print) is nothing

    def test_inspect_should_not_call_f(self, nothing: Option[int]) -> None:
        f = mock.Mock()
        nothing.inspect(f)
        f.assert_not_called()

    # ==========is_nothing==========
    def test_is_nothing_should_return_true(self, nothing: Option[int]) -> None:
        assert nothing.is_nothing() is True

    # ==========is_nothing_or==========
    def test_is_nothing_or_should_return_true(self, nothing: Option[int]) -> None:
        assert nothing.is_nothing_or(lambda _: False) is True

    def test_is_nothing_or_should_not_call_predicate(
        self, nothing: Option[int]
    ) -> None:
        predicate = mock.Mock()
        nothing.is_nothing_or(predicate)
        predicate.assert_not_called()

    # ==========is_some==========
    def test_is_some_should_return_false(self, nothing: Option[int]) -> None:
        assert nothing.is_some() is False

    # ==========is_some_and==========
    def test_is_some_and_should_return_false(self, nothing: Option[int]) -> None:
        assert nothing.is_some_and(lambda _: True) is False

    def test_is_some_and_should_not_call_predicate(self, nothing: Option[int]) -> None:
        predicate = mock.Mock()
        nothing.is_some_and(predicate)
        predicate.assert_not_called()

    # ==========map==========
    def test_map_should_return_nothing(self, nothing: Option[int]) -> None:
        assert nothing.map(lambda v: v * 2) is nothing

    # ==========map_or==========
    def test_map_or_should_return_default(self, nothing: Option[int]) -> None:
        assert nothing.map_or(0, lambda v: v * 2) == 0

    def test_map_or_should_not_call_f(self, nothing: Option[int]) -> None:
        f = mock.Mock()
        nothing.map_or(0, f)
        f.assert_not_called()

    # ==========map_or_else==========
    def test_map_or_else_should_return_result_of_default(
        self, nothing: Option[int]
    ) -> None:
        assert nothing.map_or_else(lambda: 0, lambda v: v * 2) == 0

    def test_map_or_else_should_call_default(self, nothing: Option[int]) -> None:
        default = mock.Mock()
        nothing.map_or_else(default, lambda v: v * 2)
        default.assert_called_once()

    def test_map_or_else_should_not_call_f(self, nothing: Option[int]) -> None:
        f = mock.Mock()
        nothing.map_or_else(lambda: 0, f)
        f.assert_not_called()

    # ==========ok_or==========
    def test_ok_or_should_return_err_with_err(self, nothing: Option[int]) -> None:
        assert nothing.ok_or("Failure") == Err("Failure")

    # ==========ok_or_else==========
    def test_ok_or_else_should_return_err_with_result_of_err(
        self, nothing: Option[int]
    ) -> None:
        assert nothing.ok_or_else(lambda: "Failure") == Err("Failure")

    def test_ok_or_else_should_call_err(self, nothing: Option[int]) -> None:
        err = mock.Mock()
        nothing.ok_or_else(err)
        err.assert_called_once()

    # ==========or_==========
    @pytest.mark.parametrize(
        "optb",
        [
            [Some(200)],
            [Nothing()],
        ],
    )
    def test_or_should_return_optb(
        self, nothing: Option[int], optb: Option[int]
    ) -> None:
        assert nothing.or_(optb) is optb

    # ==========or_else==========
    def test_or_else_should_return_result_of_f(self, nothing: Option[int]) -> None:
        assert nothing.or_else(lambda: Some(200)) == Some(200)

    def test_or_else_should_call_f(self, nothing: Option[int]) -> None:
        f = mock.Mock()
        nothing.or_else(f)
        f.assert_called_once()

    # ==========unwrap==========
    def test_unwrap_should_raise_UnwrapError(self, nothing: Option[int]) -> None:
        with pytest.raises(UnwrapError):
            nothing.unwrap()

    # ==========unwrap_or==========
    def test_unwrap_or_should_return_default(self, nothing: Option[int]) -> None:
        assert nothing.unwrap_or(0) == 0

    # ==========unwrap_or_else==========
    def test_unwrap_or_else_should_return_result_of_f(
        self, nothing: Option[int]
    ) -> None:
        assert nothing.unwrap_or_else(lambda: 0) == 0

    def test_unwrap_or_else_should_call_f(self, nothing: Option[int]) -> None:
        f = mock.Mock()
        nothing.unwrap_or_else(f)
        f.assert_called_once()


# ==========================================
# ===            Results                 ===
# ==========================================
class TestOk:
    # ==========and_==========
    @pytest.mark.parametrize(
        "res",
        [
            [Ok("Success")],
            [Err("Another failure")],
        ],
    )
    def test_and_should_return_res(
        self, ok: Result[int, str], res: Result[str, str]
    ) -> None:
        assert ok.and_(res) is res

    # ==========and_then==========
    def test_and_then_should_return_result_of_f(self, ok: Result[int, str]) -> None:
        assert ok.and_then(lambda v: Ok(v * 2)) == Ok(200)

    def test_and_then_should_call_f_with_wrapped_value(
        self, ok: Result[int, str]
    ) -> None:
        f = mock.Mock()
        ok.and_then(f)
        f.assert_called_once_with(100)

    # ==========expect==========
    def test_expect_should_return_contained_value(self, ok: Result[int, str]) -> None:
        assert ok.expect("Testing expect") == 100

    # ==========expect_err==========
    def test_expect_err_should_raise_UnwrapError_with_msg(
        self, ok: Result[int, str]
    ) -> None:
        with pytest.raises(UnwrapError, match="Testing expect_err"):
            ok.expect_err("Testing expect_err")

    # ==========inspect==========
    def test_inspect_should_return_self(self, ok: Result[int, str]) -> None:
        assert ok.inspect(print) is ok

    def test_inspect_should_call_f_with_wrapped_value(
        self, ok: Result[int, str]
    ) -> None:
        f = mock.Mock()
        ok.inspect(f)
        f.assert_called_once_with(100)

    # ==========inspect_err==========
    def test_inspect_err_should_return_self(self, ok: Result[int, str]) -> None:
        assert ok.inspect_err(print) is ok

    def test_inspect_err_should_not_call_f(self, ok: Result[int, str]) -> None:
        f = mock.Mock()
        ok.inspect_err(f)
        f.assert_not_called()

    # ==========unwrap==========
    def test_unwrap_should_return_contained_value(self, ok: Result[int, str]) -> None:
        assert ok.unwrap() == 100

    # ==========unwrap_err==========
    def test_unwrap_err_should_raise_UnwrapError(self, ok: Result[int, str]) -> None:
        with pytest.raises(UnwrapError):
            ok.unwrap_err()

    # ==========unwrap_or==========
    def test_unwrap_or_should_return_contained_value(
        self, ok: Result[int, str]
    ) -> None:
        assert ok.unwrap_or(0) == 100

    # ==========unwrap_or_else==========
    def test_unwrap_or_else_should_return_contained_value(
        self, ok: Result[int, str]
    ) -> None:
        assert ok.unwrap_or_else(len) == 100

    def test_unwrap_or_else_should_not_call_f(self, ok: Result[int, str]) -> None:
        f = mock.Mock()
        ok.unwrap_or_else(f)
        f.assert_not_called()


class TestErr:
    # ==========and_==========
    def test_and_should_return_self(self, err: Result[int, str]) -> None:
        assert err.and_(Ok("Success")) is err

    # ==========and_then==========
    def test_and_then_should_return_self(self, err: Result[int, str]) -> None:
        assert err.and_then(lambda v: Ok("ha" * v)) is err

    def test_and_then_should_not_call_f(self, err: Result[int, str]) -> None:
        f = mock.Mock()
        err.and_then(f)
        f.assert_not_called()

    # ==========expect==========
    def test_expect_should_raise_UnwrapError_with_msg(
        self, err: Result[int, str]
    ) -> None:
        with pytest.raises(UnwrapError, match="Testing expect"):
            err.expect("Testing expect")

    # ==========expect_err==========
    def test_expect_err_should_return_contained_value(
        self, err: Result[int, str]
    ) -> None:
        assert err.expect_err("Testing expect_err") == "Failure"

    # ==========inspect==========
    def test_inspect_should_return_self(self, err: Result[int, str]) -> None:
        assert err.inspect(print) is err

    def test_inspect_should_not_call_f(self, err: Result[int, str]) -> None:
        f = mock.Mock()
        err.inspect(f)
        f.assert_not_called()

    # ==========inspect_err==========
    def test_inspect_err_should_return_self(self, err: Result[int, str]) -> None:
        assert err.inspect_err(print) is err

    def test_inspect_err_should_call_f_with_wrapped_value(
        self, err: Result[int, str]
    ) -> None:
        f = mock.Mock()
        err.inspect_err(f)
        f.assert_called_once_with("Failure")

    # ==========unwrap==========
    def test_unwrap_should_raise_UnwrapError(self, err: Result[int, str]) -> None:
        with pytest.raises(UnwrapError):
            err.unwrap()

    # ==========unwrap_err==========
    def test_unwrap_err_should_return_contained_value(
        self, err: Result[int, str]
    ) -> None:
        assert err.unwrap_err() == "Failure"

    # ==========unwrap_or==========
    def test_unwrap_or_should_return_default(self, err: Result[int, str]) -> None:
        assert err.unwrap_or(0) == 0

    # ==========unwrap_or_else==========
    def test_unwrap_or_else_should_return_result_of_f(
        self, err: Result[int, str]
    ) -> None:
        assert err.unwrap_or_else(len) == 7

    def test_unwrap_or_else_should_call_f_with_wrapped_value(
        self, err: Result[int, str]
    ) -> None:
        f = mock.Mock()
        err.unwrap_or_else(f)
        f.assert_called_once_with("Failure")
