from unittest import mock

import pytest

from bento import Map, MutMap, Nothing, Option, Some


# ==========================================
# ===            Fixtures                ===
# ==========================================
@pytest.fixture
def map() -> Map[str, int]:
    return Map({"a": 1, "b": 2, "c": 3})


@pytest.fixture
def mut_map() -> MutMap[str, int]:
    return MutMap({"a": 1, "b": 2, "c": 3})


# ==========================================
# ===            Maps                    ===
# ==========================================
class TestMap:
    # ==========get==========
    @pytest.mark.parametrize(
        "key, expected_value",
        [
            ["a", Some(1)],
            ["b", Some(2)],
            ["c", Some(3)],
            ["d", Nothing()],
        ],
    )
    def test_get_should_return_expected_value(
        self, map: Map[str, int], key: str, expected_value: Option[int]
    ) -> None:
        assert map.get(key) == expected_value

    def test_get_should_return_nothing_if_map_is_empty(self) -> None:
        assert Map[str, int]().get("testing") == Nothing()

    # ==========get_or==========
    @pytest.mark.parametrize(
        "key, expected_value",
        [
            ["a", 1],
            ["b", 2],
            ["c", 3],
            ["d", 0],
        ],
    )
    def test_get_or_should_return_expected_value(
        self, map: Map[str, int], key: str, expected_value: int
    ) -> None:
        assert map.get_or(0, key) == expected_value

    # ==========get_or_else==========
    @pytest.mark.parametrize(
        "key, expected_value",
        [
            ["a", 1],
            ["b", 2],
            ["c", 3],
            ["d", 0],
        ],
    )
    def test_get_or_else_should_return_expected_value(
        self, map: Map[str, int], key: str, expected_value: int
    ) -> None:
        assert map.get_or_else(lambda: 0, key) == expected_value

    def test_get_or_else_should_call_f_if_key_not_in_map(
        self, map: Map[str, int]
    ) -> None:
        f = mock.Mock()
        map.get_or_else(f, "d")
        f.assert_called_once()

    def test_get_or_else_should_not_call_f_if_key_in_map(
        self, map: Map[str, int]
    ) -> None:
        f = mock.Mock()
        map.get_or_else(f, "a")
        f.assert_not_called()


class TestMutMap:
    # ==========get==========
    def test_get_should_return_nothing_if_mut_map_is_empty(self) -> None:
        assert MutMap[str, int]().get("testing") == Nothing()
