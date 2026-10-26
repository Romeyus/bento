from typing import Any
from unittest import mock

import pytest

from bento import Nothing, Option, Panic, Some


# ==========================================
# ===            Fixtures                ===
# ==========================================
@pytest.fixture
def some() -> Option[int]:
    return Some(100)


@pytest.fixture
def nothing() -> Option[int]:
    return Nothing()


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
    def test_expect_should_raise_Panic_exception_with_msg(
        self, nothing: Option[int]
    ) -> None:
        with pytest.raises(Panic, match="Testing expect"):
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
