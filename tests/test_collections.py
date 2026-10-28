from unittest import mock

import pytest

from bento import Map, MutMap, MutVec, Nothing, Option, Some, Vec


# ==========================================
# ===            Fixtures                ===
# ==========================================
@pytest.fixture
def map() -> Map[str, int]:
    return Map({"a": 1, "b": 2, "c": 3})


@pytest.fixture
def mut_map() -> MutMap[str, int]:
    return MutMap({"a": 1, "b": 2, "c": 3})


@pytest.fixture
def vec() -> Vec[str]:
    return Vec(["a", "b", "c"])


@pytest.fixture
def mut_vec() -> MutVec[str]:
    return MutVec(["a", "b", "c"])


# ==========================================
# ===            Maps                    ===
# ==========================================
class TestMap:
    # ==========copy==========
    def test_copy_should_return_shallow_copy_of_self(self, map: Map[str, int]) -> None:
        assert map.copy() == map

    def test_copy_should_not_return_self(self, map: Map[str, int]) -> None:
        assert map.copy() is not map

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

    # ==========items==========
    def test_items_should_return_iterable_of_tuple_of_key_and_value(
        self, map: Map[str, int]
    ) -> None:
        assert list(map.items()) == [("a", 1), ("b", 2), ("c", 3)]

    # ==========keys==========
    def test_keys_should_return_iterable_of_keys(self, map: Map[str, int]) -> None:
        assert list(map.keys()) == ["a", "b", "c"]

    # ==========values==========
    def test_values_should_return_iterable_of_values(self, map: Map[str, int]) -> None:
        assert list(map.values()) == [1, 2, 3]

    # ==========__contains__==========
    @pytest.mark.parametrize(
        "key, expected_value",
        [
            ["a", True],
            ["b", True],
            ["c", True],
            ["d", False],
        ],
    )
    def test__contains__should_return_expected_value(
        self, map: Map[str, int], key: str, expected_value: bool
    ) -> None:
        assert (key in map) is expected_value

    # ==========__eq__==========
    @pytest.mark.parametrize(
        "other, expected_value",
        [
            [Map({"a": 1, "b": 2, "c": 3}), True],
            [Map[str, int](), False],
            ["failure", False],
            [100, False],
        ],
    )
    def test__eq__should_return_expected_value(
        self, map: Map[str, int], other: object, expected_value: bool
    ) -> None:
        assert (map == other) is expected_value

    # ==========__iter__==========
    def test__iter__should_return_iterator_of_keys(self, map: Map[str, int]) -> None:
        assert list(iter(map)) == ["a", "b", "c"]

    # ==========__len__==========
    def test__len__should_return_nb_of_keys(self, map: Map[str, int]) -> None:
        assert len(map) == 3


class TestMutMap:
    # ==========copy==========
    def test_copy_should_return_shallow_copy_of_self(
        self, mut_map: MutMap[str, int]
    ) -> None:
        assert mut_map.copy() == mut_map

    # ==========get==========
    def test_get_should_return_nothing_if_mut_map_is_empty(self) -> None:
        assert MutMap[str, int]().get("testing") == Nothing()

    # ==========get_or_set==========
    def test_get_or_set_should_return_default_if_key_not_in_map(
        self, mut_map: MutMap[str, int]
    ) -> None:
        assert mut_map.get_or_set(0, "d") == 0

    def test_get_or_set_should_set_new_value_corresponding_to_key_if_key_not_in_map(
        self, mut_map: MutMap[str, int]
    ) -> None:
        mut_map.get_or_set(0, "d")
        assert mut_map.get("d") == Some(0)

    def test_get_or_set_should_return_value_corresponding_to_key_if_key_in_map(
        self, mut_map: MutMap[str, int]
    ) -> None:
        assert mut_map.get_or_set(0, "a") == 1

    def test_get_or_set_should_not_set_new_value_if_key_in_map(
        self, mut_map: MutMap[str, int]
    ) -> None:
        mut_map.get_or_set(0, "a")
        assert mut_map.get("a") == Some(1)

    # ==========get_or_else_set==========
    def test_get_or_else_set_should_return_result_of_f_if_key_not_in_map(
        self, mut_map: MutMap[str, int]
    ) -> None:
        assert mut_map.get_or_else_set(lambda: 0, "d") == 0

    def test_get_or_else_set_should_set_new_value_corresponding_to_key_if_key_not_in_map(
        self, mut_map: MutMap[str, int]
    ) -> None:
        mut_map.get_or_else_set(lambda: 0, "d")
        assert mut_map.get("d") == Some(0)

    def test_get_or_else_set_should_call_f_if_key_not_in_map(
        self, mut_map: MutMap[str, int]
    ) -> None:
        f = mock.Mock()
        mut_map.get_or_else_set(f, "d")
        f.assert_called_once()

    def test_get_or_else_set_should_return_value_corresponding_to_key_if_key_in_map(
        self, mut_map: MutMap[str, int]
    ) -> None:
        assert mut_map.get_or_else_set(lambda: 0, "a") == 1

    def test_get_or_else_set_should_not_set_new_value_if_key_in_map(
        self, mut_map: MutMap[str, int]
    ) -> None:
        mut_map.get_or_else_set(lambda: 0, "a")
        assert mut_map.get("a") == Some(1)

    def test_get_or_else_set_should_not_call_f_if_key_in_map(
        self, mut_map: MutMap[str, int]
    ) -> None:
        f = mock.Mock()
        mut_map.get_or_else_set(f, "a")
        f.assert_not_called()

    # ==========pop==========
    @pytest.mark.parametrize(
        "key, expected_value",
        [
            ["a", Some(1)],
            ["b", Some(2)],
            ["c", Some(3)],
            ["d", Nothing()],
        ],
    )
    def test_pop_should_return_expected_value(
        self, mut_map: MutMap[str, int], key: str, expected_value: Option[int]
    ) -> None:
        assert mut_map.pop(key) == expected_value

    def test_pop_should_remove_key_from_map_if_key_in_map(
        self, mut_map: MutMap[str, int]
    ) -> None:
        mut_map.pop("a")
        assert "a" not in mut_map

    # ==========pop_or==========
    @pytest.mark.parametrize(
        "key, expected_value",
        [
            ["a", 1],
            ["b", 2],
            ["c", 3],
            ["d", 0],
        ],
    )
    def test_pop_or_should_return_expected_value(
        self, mut_map: MutMap[str, int], key: str, expected_value: int
    ) -> None:
        assert mut_map.pop_or(0, key) == expected_value

    def test_pop_or_should_remove_key_from_map_if_key_in_map(
        self, mut_map: MutMap[str, int]
    ) -> None:
        mut_map.pop_or(0, "a")
        assert "a" not in mut_map

    # ==========pop_or_else==========
    @pytest.mark.parametrize(
        "key, expected_value",
        [
            ["a", 1],
            ["b", 2],
            ["c", 3],
            ["d", 0],
        ],
    )
    def test_pop_or_else_should_return_expected_value(
        self, mut_map: MutMap[str, int], key: str, expected_value: int
    ) -> None:
        assert mut_map.pop_or_else(lambda: 0, key) == expected_value

    def test_pop_or_else_should_remove_key_from_map_if_key_in_map(
        self, mut_map: MutMap[str, int]
    ) -> None:
        mut_map.pop_or_else(lambda: 0, "a")
        assert "a" not in mut_map

    def test_pop_or_else_should_call_f_if_key_not_in_map(
        self, mut_map: MutMap[str, int]
    ) -> None:
        f = mock.Mock()
        mut_map.pop_or_else(f, "d")
        f.assert_called_once()

    def test_pop_or_else_should_not_call_f_if_key_in_map(
        self, mut_map: MutMap[str, int]
    ) -> None:
        f = mock.Mock()
        mut_map.pop_or_else(f, "a")
        f.assert_not_called()

    # ==========__setitem__==========
    @pytest.mark.parametrize(
        "key",
        ["a", "b", "c", "d"],
    )
    def test__setitem__should_set_new_value_corresponding_to_key(
        self, mut_map: MutMap[str, int], key: str
    ) -> None:
        mut_map[key] = 0
        assert mut_map.get(key) == Some(0)


# ==========================================
# ===            Vectors                 ===
# ==========================================
class TestVec:
    # ==========copy==========
    def test_copy_should_return_shallow_copy_of_self(self, vec: Vec[str]) -> None:
        assert vec.copy() == vec

    def test_copy_should_not_return_self(self, vec: Vec[str]) -> None:
        assert vec.copy() is not vec

    # ==========get==========
    @pytest.mark.parametrize(
        "index, expected_value",
        [
            [0, Some("a")],
            [1, Some("b")],
            [2, Some("c")],
            [3, Nothing()],
            [-1, Some("c")],
            [-2, Some("b")],
            [-3, Some("a")],
            [-4, Nothing()],
        ],
    )
    def test_get_should_return_expected_value(
        self, vec: Vec[str], index: int, expected_value: Option[str]
    ) -> None:
        assert vec.get(index) == expected_value

    def test_get_should_return_nothing_if_vec_is_empty(self) -> None:
        assert Vec[str]().get(100) == Nothing()

    # ==========get_or==========
    @pytest.mark.parametrize(
        "index, expected_value",
        [
            [0, "a"],
            [1, "b"],
            [2, "c"],
            [3, "d"],
            [-1, "c"],
            [-2, "b"],
            [-3, "a"],
            [-4, "d"],
        ],
    )
    def test_get_or_should_return_expected_value(
        self, vec: Vec[str], index: int, expected_value: str
    ) -> None:
        assert vec.get_or("d", index) == expected_value

    # ==========get_or_else==========
    @pytest.mark.parametrize(
        "index, expected_value",
        [
            [0, "a"],
            [1, "b"],
            [2, "c"],
            [3, "d"],
            [-1, "c"],
            [-2, "b"],
            [-3, "a"],
            [-4, "d"],
        ],
    )
    def test_get_or_else_should_return_expected_value(
        self, vec: Vec[str], index: int, expected_value: str
    ) -> None:
        assert vec.get_or_else(lambda: "d", index) == expected_value

    def test_get_or_else_should_not_call_f_if_index_in_range(
        self, vec: Vec[str]
    ) -> None:
        f = mock.Mock()
        vec.get_or_else(f, 0)
        f.assert_not_called()

    def test_get_or_else_should_call_f_if_index_out_of_range(
        self, vec: Vec[str]
    ) -> None:
        f = mock.Mock()
        vec.get_or_else(f, 4)
        f.assert_called_once()

    # ==========__contains__==========
    @pytest.mark.parametrize(
        "value, expected_value",
        [
            ["a", True],
            ["b", True],
            ["c", True],
            ["d", False],
        ],
    )
    def test__contains__should_return_expected_value(
        self, vec: Vec[str], value: str, expected_value: bool
    ) -> None:
        assert (value in vec) is expected_value

    # ==========__eq__==========
    @pytest.mark.parametrize(
        "other, expected_value",
        [
            [Vec(["a", "b", "c"]), True],
            [Vec[str](), False],
            ["failure", False],
            [100, False],
        ],
    )
    def test__eq__should_return_expected_value(
        self, vec: Vec[str], other: object, expected_value: bool
    ) -> None:
        assert (vec == other) is expected_value

    # ==========__iter__==========
    def test__iter__should_return_iterator_of_values(self, vec: Vec[str]) -> None:
        assert list(iter(vec)) == ["a", "b", "c"]

    # ==========__len__==========
    def test__len__should_return_nb_of_values(self, vec: Vec[str]) -> None:
        assert len(vec) == 3


class TestMutVec:
    # ==========copy==========
    def test_copy_should_return_shallow_copy_of_self(
        self, mut_vec: MutVec[str]
    ) -> None:
        assert mut_vec.copy() == mut_vec

    # ==========get==========
    def test_get_should_return_nothing_if_vec_is_empty(self) -> None:
        assert MutVec[str]().get(100) == Nothing()
