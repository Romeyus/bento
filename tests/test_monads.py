from unittest import mock

import pytest

from bento import Err, Nothing, Ok, Option, Result, Some, UnwrapError


# ==========================================
# ===            Options                 ===
# ==========================================
class TestSome:
    @pytest.fixture
    def opt(self) -> Option[int]:
        return Some(100)

    # ==========test_and_==========
    @pytest.mark.parametrize(
        "optb",
        [Some("Hello world!"), Nothing()],
    )
    def test_and_should_return_optb(self, opt: Option[int], optb: Option[str]) -> None:
        assert opt.and_(optb) is optb

    # ==========test_and_then==========
    def test_and_then_should_return_f_product(self, opt: Option[int]) -> None:
        assert opt.and_then(lambda x: Some(x * 2)) == Some(200)

    def test_and_then_should_call_f_with_contained_value(
        self, opt: Option[int]
    ) -> None:
        f = mock.Mock()
        opt.and_then(f)
        f.assert_called_once_with(100)

    # ==========test_expect==========
    def test_expect_should_return_contained_value(self, opt: Option[int]) -> None:
        assert opt.expect("testing expect") == 100

    # ==========test_filter==========
    @pytest.mark.parametrize(
        "value, expected",
        [
            [True, Some(100)],
            [False, Nothing()],
        ],
    )
    def test_filter_should_return_expected(
        self, opt: Option[int], value: bool, expected: Option[int]
    ) -> None:
        assert opt.filter(lambda _: value) == expected

    def test_filter_should_call_predicate_with_contained_value(
        self, opt: Option[int]
    ) -> None:
        predicate = mock.Mock()
        opt.filter(predicate)
        predicate.assert_called_once_with(100)

    # ==========test_map==========
    def test_map_should_return_some_containing_f_product(
        self, opt: Option[int]
    ) -> None:
        assert opt.map(lambda x: x * 2) == Some(200)

    def test_map_should_call_f_with_contained_value(self, opt: Option[int]) -> None:
        f = mock.Mock()
        opt.map(f)
        f.assert_called_once_with(100)

    # ==========test_map_or==========
    def test_map_or_should_return_f_product(self, opt: Option[int]) -> None:
        assert opt.map_or(1000, lambda x: x * 2) == 200

    def test_map_or_should_call_f_with_contained_value(self, opt: Option[int]) -> None:
        f = mock.Mock()
        opt.map_or(1000, f)
        f.assert_called_once_with(100)

    # ==========test_map_or_else==========
    def test_map_or_else_should_return_f_product(self, opt: Option[int]) -> None:
        assert opt.map_or_else(lambda: 1000, lambda x: x * 2) == 200

    def test_map_or_else_should_call_f_with_contained_value(
        self, opt: Option[int]
    ) -> None:
        f = mock.Mock()
        opt.map_or_else(lambda: 1000, f)
        f.assert_called_once_with(100)

    def test_map_or_else_should_not_call_default(self, opt: Option[int]) -> None:
        default = mock.Mock()
        opt.map_or_else(default, lambda x: x * 2)
        default.assert_not_called()

    # ==========test_ok_or==========
    def test_ok_or_should_return_ok_containing_self_value(
        self, opt: Option[int]
    ) -> None:
        assert opt.ok_or("Something went wrong!") == Ok(100)

    # ==========test_ok_or_else==========
    def test_ok_or_else_should_return_ok_containing_self_value(
        self, opt: Option[int]
    ) -> None:
        assert opt.ok_or_else(lambda: "Something went wrong!") == Ok(100)

    def test_ok_or_else_should_not_call_f(self, opt: Option[int]) -> None:
        f = mock.Mock()
        opt.ok_or_else(f)
        f.assert_not_called()

    # ==========test_or_==========
    @pytest.mark.parametrize(
        "optb",
        [Some(200), Nothing()],
    )
    def test_or_should_return_self(self, opt: Option[int], optb: Option[int]) -> None:
        assert opt.or_(optb) is opt

    # ==========test_or_else==========
    def test_or_else_should_return_self(self, opt: Option[int]) -> None:
        assert opt.or_else(lambda: Some(200)) is opt

    def test_test_or_else_should_not_call_f(self, opt: Option[int]) -> None:
        f = mock.Mock()
        opt.or_else(f)
        f.assert_not_called()

    # ==========test_unwrap==========
    def test_unwrap_should_return_self_value(self, opt: Option[int]) -> None:
        assert opt.unwrap() == 100

    # ==========test_unwrap_or==========
    def test_unwrap_or_should_return_self_value(self, opt: Option[int]) -> None:
        assert opt.unwrap_or(1000) == 100

    # ==========test_unwrap_or_else==========
    def test_unwrap_or_else_should_return_self_value(self, opt: Option[int]) -> None:
        assert opt.unwrap_or_else(lambda: 1000) == 100

    def test_unwrap_or_else_should_not_call_f(self, opt: Option[int]) -> None:
        f = mock.Mock()
        opt.unwrap_or_else(f)
        f.assert_not_called()


class TestNothing:
    @pytest.fixture
    def opt(self) -> Option[int]:
        return Nothing()

    # ==========test_and_==========
    @pytest.mark.parametrize(
        "optb",
        [Some(200), Nothing()],
    )
    def test_and_should_return_self(self, opt: Option[int], optb: Option[str]) -> None:
        assert opt.and_(optb) is opt

    # ==========test_and_then==========
    def test_and_then_should_return_self(self, opt: Option[int]) -> None:
        assert opt.and_then(lambda x: Some(x * 2)) is opt

    def test_and_then_should_not_call_f(self, opt: Option[int]) -> None:
        f = mock.Mock()
        opt.and_then(f)
        f.assert_not_called()

    # ==========test_expect==========
    def test_expect_should_raise_unwrap_error_containing_msg(
        self, opt: Option[int]
    ) -> None:
        with pytest.raises(UnwrapError, match="testing expect"):
            opt.expect("testing expect")

    # ==========test_filter==========
    @pytest.mark.parametrize(
        "value",
        [True, False],
    )
    def test_filter_should_return_self(self, opt: Option[int], value: bool) -> None:
        assert opt.filter(lambda _: value) is opt

    def test_filter_should_not_call_predicate(self, opt: Option[int]) -> None:
        predicate = mock.Mock()
        opt.filter(predicate)
        predicate.assert_not_called()

    # ==========test_map==========
    def test_map_should_return_self(self, opt: Option[int]) -> None:
        assert opt.map(lambda x: x * 2) is opt

    def test_map_should_not_call_f(self, opt: Option[int]) -> None:
        f = mock.Mock()
        opt.map(f)
        f.assert_not_called()

    # ==========test_map_or==========
    def test_map_or_should_return_default(self, opt: Option[int]) -> None:
        assert opt.map_or(1000, lambda x: x * 2) == 1000

    def test_map_or_should_not_call_f(self, opt: Option[int]) -> None:
        f = mock.Mock()
        opt.map_or(1000, f)
        f.assert_not_called()

    # ==========test_map_or_else==========
    def test_map_or_else_should_return_default_product(self, opt: Option[int]) -> None:
        assert opt.map_or_else(lambda: 1000, lambda x: x * 2) == 1000

    def test_map_or_else_should_call_default(self, opt: Option[int]) -> None:
        default = mock.Mock()
        opt.map_or_else(default, lambda x: x * 2)
        default.assert_called_once()

    def test_map_or_else_should_not_call_f(self, opt: Option[int]) -> None:
        f = mock.Mock()
        opt.map_or_else(lambda: 1000, f)
        f.assert_not_called()

    # ==========test_ok_or==========
    def test_ok_or_should_return_err_containing_e(self, opt: Option[int]) -> None:
        assert opt.ok_or("Something went wrong!") == Err("Something went wrong!")

    # ==========test_ok_or_else==========
    def test_ok_or_else_should_return_err_containing_f_product(
        self, opt: Option[int]
    ) -> None:
        assert opt.ok_or_else(lambda: "Something went wrong!") == Err(
            "Something went wrong!"
        )

    def test_ok_or_else_should_call_f(self, opt: Option[int]) -> None:
        f = mock.Mock()
        opt.ok_or_else(f)
        f.assert_called_once()

    # ==========test_or_==========
    @pytest.mark.parametrize(
        "optb",
        [Some(200), Nothing()],
    )
    def test_or_should_return_optb(self, opt: Option[int], optb: Option[int]) -> None:
        assert opt.or_(optb) is optb

    # ==========test_or_else==========
    def test_or_else_should_return_f_product(self, opt: Option[int]) -> None:
        assert opt.or_else(lambda: Some(200)) == Some(200)

    def test_or_else_should_call_f(self, opt: Option[int]) -> None:
        f = mock.Mock()
        opt.or_else(f)
        f.assert_called_once()

    # ==========test_unwrap==========
    def test_unwrap_should_raise_unwrap_error(self, opt: Option[int]) -> None:
        with pytest.raises(UnwrapError):
            opt.unwrap()

    # ==========test_unwrap_or==========
    def test_unwrap_or_should_return_default(self, opt: Option[int]) -> None:
        assert opt.unwrap_or(1000) == 1000

    # ==========test_unwrap_or_else==========
    def test_unwrap_or_else_should_return_f_product(self, opt: Option[int]) -> None:
        assert opt.unwrap_or_else(lambda: 1000) == 1000

    def test_unwrap_or_else_should_call_f(self, opt: Option[int]) -> None:
        f = mock.Mock()
        opt.unwrap_or_else(f)
        f.assert_called_once()


# ==========================================
# ===            Results                 ===
# ==========================================
class TestOk:
    @pytest.fixture
    def res(self) -> Result[int, str]:
        return Ok(100)

    # ==========test_and_==========
    @pytest.mark.parametrize(
        "resb",
        [Ok(100.5), Err("Not a float")],
    )
    def test_and_should_return_resb(
        self, res: Result[int, str], resb: Result[float, str]
    ) -> None:
        assert res.and_(resb) is resb

    # ==========test_and_then==========
    def test_and_then_should_return_f_product(self, res: Result[int, str]) -> None:
        assert res.and_then(lambda x: Ok(x + 0.5)) == Ok(100.5)

    def test_and_then_should_call_f_with_contained_value(
        self, res: Result[int, str]
    ) -> None:
        f = mock.Mock()
        res.and_then(f)
        f.assert_called_once_with(100)

    # ==========test_err==========
    def test_err_should_return_nothing(self, res: Result[int, str]) -> None:
        assert res.err() == Nothing()

    # ==========test_expect==========
    def test_expect_should_return_contained_value(self, res: Result[int, str]) -> None:
        assert res.expect("testing expect") == 100

    # ==========test_expect_err==========
    def test_expect_err_should_raise_unwrap_error_containing_msg(
        self, res: Result[int, str]
    ) -> None:
        with pytest.raises(UnwrapError, match="testing expect_err"):
            res.expect_err("testing expect_err")

    # ==========test_map==========
    def test_map_should_return_ok_containing_f_product(
        self, res: Result[int, str]
    ) -> None:
        assert res.map(lambda x: x * 2) == Ok(200)

    def test_map_should_call_f_with_contained_value(
        self, res: Result[int, str]
    ) -> None:
        f = mock.Mock()
        res.map(f)
        f.assert_called_once_with(100)

    # ==========test_map_err==========
    def test_map_err_should_return_self(self, res: Result[int, str]) -> None:
        assert res.map_err(str.upper) is res

    def test_map_err_should_not_call_f(self, res: Result[int, str]) -> None:
        f = mock.Mock()
        res.map_err(f)
        f.assert_not_called()

    # ==========test_map_or==========
    def test_map_or_should_return_f_product(self, res: Result[int, str]) -> None:
        assert res.map_or(1000, lambda x: x * 2) == 200

    def test_map_or_should_call_f_with_contained_value(
        self, res: Result[int, str]
    ) -> None:
        f = mock.Mock()
        res.map_or(1000, f)
        f.assert_called_once_with(100)

    # ==========test_map_or_else==========
    def test_map_or_else_should_return_f_product(self, res: Result[int, str]) -> None:
        assert res.map_or_else(len, lambda x: x * 2) == 200

    def test_map_or_else_should_call_f_with_contained_value(
        self, res: Result[int, str]
    ) -> None:
        f = mock.Mock()
        res.map_or_else(len, f)
        f.assert_called_once_with(100)

    def test_map_or_else_should_not_call_default(self, res: Result[int, str]) -> None:
        default = mock.Mock()
        res.map_or_else(default, lambda x: x * 2)
        default.assert_not_called()

    # ==========test_ok==========
    def test_ok_should_return_some_containing_self_value(
        self, res: Result[int, str]
    ) -> None:
        assert res.ok() == Some(100)

    # ==========test_or_==========
    @pytest.mark.parametrize(
        "resb",
        [Ok(200), Err(500)],
    )
    def test_or_should_return_self(
        self, res: Result[int, str], resb: Result[int, int]
    ) -> None:
        assert res.or_(resb) is res

    # ==========test_or_else==========
    def test_or_else_should_return_self(self, res: Result[int, str]) -> None:
        assert res.or_else(lambda e: Err(len(e))) is res

    def test_or_else_should_not_call_f(self, res: Result[int, str]) -> None:
        f = mock.Mock()
        res.or_else(f)
        f.assert_not_called()

    # ==========test_unwrap==========
    def test_unwrap_should_return_contained_value(self, res: Result[int, str]) -> None:
        assert res.unwrap() == 100

    # ==========test_unwrap_err==========
    def test_unwrap_err_should_raise_unwrap_error(self, res: Result[int, str]) -> None:
        with pytest.raises(UnwrapError):
            res.unwrap_err()

    # ==========test_unwrap_or==========
    def test_unwrap_or_should_return_contained_value(
        self, res: Result[int, str]
    ) -> None:
        assert res.unwrap_or(1000) == 100

    # ==========test_unwrap_or_else==========
    def test_unwrap_or_else_should_return_contained_value(
        self, res: Result[int, str]
    ) -> None:
        assert res.unwrap_or_else(len) == 100

    def test_unwrap_or_else_should_not_call_f(self, res: Result[int, str]) -> None:
        f = mock.Mock()
        res.unwrap_or_else(f)
        f.assert_not_called()


class TestErr:
    @pytest.fixture
    def res(self) -> Result[int, str]:
        return Err("Failure")

    # ==========test_and_==========
    @pytest.mark.parametrize(
        "resb",
        [Ok("Hello world!"), Err("Something went wrong!")],
    )
    def test_and_should_return_self(
        self, res: Result[int, str], resb: Result[str, str]
    ) -> None:
        assert res.and_(resb) is res

    # ==========test_and_then==========
    def test_and_then_should_return_self(self, res: Result[int, str]) -> None:
        assert res.and_then(lambda x: Ok(x * 2)) is res

    def test_and_then_should_not_call_f(self, res: Result[int, str]) -> None:
        f = mock.Mock()
        res.and_then(f)
        f.assert_not_called()

    # ==========test_err==========
    def test_err_should_return_some_containing_self_value(
        self, res: Result[int, str]
    ) -> None:
        assert res.err() == Some("Failure")

    # ==========test_expect==========
    def test_expect_should_raise_unwrap_error_containing_msg(
        self, res: Result[int, str]
    ) -> None:
        with pytest.raises(UnwrapError, match="testing expect"):
            res.expect("testing expect")

    # ==========test_expect_err==========
    def test_expect_err_should_return_contained_value(
        self, res: Result[int, str]
    ) -> None:
        assert res.expect_err("testing expect_err") == "Failure"

    # ==========test_map==========
    def test_map_should_return_self(self, res: Result[int, str]) -> None:
        assert res.map(lambda x: x * 2) is res

    def test_map_should_not_call_f(self, res: Result[int, str]) -> None:
        f = mock.Mock()
        res.map(f)
        f.assert_not_called()

    # ==========test_map_err==========
    def test_map_err_should_return_err_containing_f_product(
        self, res: Result[int, str]
    ) -> None:
        assert res.map_err(str.upper) == Err("FAILURE")

    def test_map_err_should_call_f_with_contained_value(
        self, res: Result[int, str]
    ) -> None:
        f = mock.Mock()
        res.map_err(f)
        f.assert_called_once_with("Failure")

    # ==========test_map_or==========
    def test_map_or_should_return_default(self, res: Result[int, str]) -> None:
        assert res.map_or(1000, lambda x: x * 2) == 1000

    def test_map_or_should_not_call_f(self, res: Result[int, str]) -> None:
        f = mock.Mock()
        res.map_or(1000, f)
        f.assert_not_called()

    # ==========test_map_or_else==========
    def test_map_or_else_should_return_default_product(
        self, res: Result[int, str]
    ) -> None:
        assert res.map_or_else(len, lambda x: x * 2) == 7

    def test_map_or_else_should_call_default_with_contained_value(
        self, res: Result[int, str]
    ) -> None:
        default = mock.Mock()
        res.map_or_else(default, lambda x: x * 2)
        default.assert_called_once_with("Failure")

    def test_map_or_else_should_not_call_f(self, res: Result[int, str]) -> None:
        f = mock.Mock()
        res.map_or_else(len, f)
        f.assert_not_called()

    # ==========test_ok==========
    def test_ok_should_return_nothing(self, res: Result[int, str]) -> None:
        assert res.ok() == Nothing()

    # ==========test_or_==========
    @pytest.mark.parametrize(
        "resb",
        [Ok(200), Err(500)],
    )
    def test_or_should_return_resb(
        self, res: Result[int, str], resb: Result[int, int]
    ) -> None:
        assert res.or_(resb) is resb

    # ==========test_or_else==========
    def test_or_else_should_return_f_product(self, res: Result[int, str]) -> None:
        assert res.or_else(lambda e: Err(len(e))) == Err(7)

    def test_or_else_should_call_f_with_contained_value(
        self, res: Result[int, str]
    ) -> None:
        f = mock.Mock()
        res.or_else(f)
        f.assert_called_once_with("Failure")

    # ==========test_unwrap==========
    def test_unwrap_should_raise_unwrap_error(self, res: Result[int, str]) -> None:
        with pytest.raises(UnwrapError):
            res.unwrap()

    # ==========test_unwrap_err==========
    def test_unwrap_err_should_return_contained_value(
        self, res: Result[int, str]
    ) -> None:
        assert res.unwrap_err() == "Failure"

    # ==========test_unwrap_or==========
    def test_unwrap_or_should_return_default(self, res: Result[int, str]) -> None:
        assert res.unwrap_or(1000) == 1000

    # ==========test_unwrap_or_else==========
    def test_unwrap_or_else_should_return_f_product(
        self, res: Result[int, str]
    ) -> None:
        assert res.unwrap_or_else(len) == 7

    def test_unwrap_or_else_should_call_f_with_contained_value(
        self, res: Result[int, str]
    ) -> None:
        f = mock.Mock()
        res.unwrap_or_else(f)
        f.assert_called_once_with("Failure")
