from unittest import mock

import pytest

from bento import Map, MutMap, MutVec, Nothing, Option, Some, Vec


# ==========================================
# ===            Maps                    ===
# ==========================================
class TestMap:
    @pytest.fixture
    def map(self) -> Map[str, int]:
        return Map({"a": 1, "b": 2, "c": 3})

    # ==========test__init__==========
    def test__init__should_set_data_to_empty_dict_if_not_provided(self) -> None:
        assert Map[str, int]() == Map[str, int]({})

    # ==========test__contains__==========
    @pytest.mark.parametrize(
        "value, expected",
        [
            ("a", True),
            ("b", True),
            ("c", True),
            ("d", False),
            ("z", False),
        ],
    )
    def test__contains__should_return_expected(
        self, map: Map[str, int], value: str, expected: bool
    ) -> None:
        assert (value in map) is expected

    # ==========test__eq__==========
    @pytest.mark.parametrize(
        "value, expected",
        [
            (Map({"a": 1, "b": 2, "c": 3}), True),
            (Map({"a": 1, "b": 2, "c": 4}), False),
            (Map({"x": 24, "y": 25, "z": 26}), False),
            ("Hello world!", False),
            (100, False),
        ],
    )
    def test__eq__should_return_expected(
        self, map: Map[str, int], value: object, expected: bool
    ) -> None:
        assert (map == value) is expected

    # ==========test__getitem__==========
    def test__getitem__should_return_corresponding_value_if_key_in_map(
        self, map: Map[str, int]
    ) -> None:
        assert map["a"] == 1

    def test__getitem__should_raise_key_error_if_key_not_in_map(
        self, map: Map[str, int]
    ) -> None:
        with pytest.raises(KeyError):
            map["z"]

    # ==========test__iter__==========
    def test__iter__should_return_key_iterator(self, map: Map[str, int]) -> None:
        assert tuple(iter(map)) == ("a", "b", "c")

    # ==========test__len__==========
    def test__len__should_return_length(self, map: Map[str, int]) -> None:
        assert len(map) == 3

    # ==========test_get==========
    @pytest.mark.parametrize(
        "key, expected",
        [
            ("a", Some(1)),
            ("b", Some(2)),
            ("c", Some(3)),
            ("d", Nothing()),
            ("z", Nothing()),
        ],
    )
    def test_get_should_return_expected(
        self, map: Map[str, int], key: str, expected: Option[int]
    ) -> None:
        assert map.get(key) == expected

    # ==========test_get_or==========
    @pytest.mark.parametrize(
        "key, expected",
        [
            ("a", 1),
            ("b", 2),
            ("c", 3),
            ("d", 1000),
            ("z", 1000),
        ],
    )
    def test_get_or_should_return_expected(
        self, map: Map[str, int], key: str, expected: int
    ) -> None:
        assert map.get_or(1000, key) == expected

    # ==========test_get_or_else==========
    @pytest.mark.parametrize(
        "key, expected",
        [
            ("a", 1),
            ("b", 2),
            ("c", 3),
            ("d", 1000),
            ("z", 1000),
        ],
    )
    def test_get_or_else_should_return_expected(
        self, map: Map[str, int], key: str, expected: int
    ) -> None:
        assert map.get_or_else(lambda: 1000, key) == expected

    def test_get_or_else_should_not_call_f_if_key_in_map(
        self, map: Map[str, int]
    ) -> None:
        f = mock.Mock()
        map.get_or_else(f, "a")
        f.assert_not_called()

    def test_get_or_else_should_call_f_if_key_not_in_map(
        self, map: Map[str, int]
    ) -> None:
        f = mock.Mock()
        map.get_or_else(f, "z")
        f.assert_called_once()

    # ==========test_items==========
    def test_items_should_return_items_view(self, map: Map[str, int]) -> None:
        assert tuple(map.items()) == (("a", 1), ("b", 2), ("c", 3))

    # ==========test_keys==========
    def test_keys_should_return_keys_view(self, map: Map[str, int]) -> None:
        assert tuple(map.keys()) == ("a", "b", "c")

    # ==========test_values==========
    def test_values_should_return_values_view(self, map: Map[str, int]) -> None:
        assert tuple(map.values()) == (1, 2, 3)


class TestMutMap:
    @pytest.fixture
    def map(self) -> MutMap[str, int]:
        return MutMap({"a": 1, "b": 2, "c": 3})

    # ==========test__init__==========
    def test__init__should_set_data_to_empty_dict_if_not_provided(self) -> None:
        assert MutMap[str, int]() == MutMap[str, int]({})

    # ==========test__setitem__==========
    @pytest.mark.parametrize(
        "key, value",
        [
            ("d", 4),
            ("z", 26),
            ("a", 101),
        ],
    )
    def test__setitem__should_set_value_at_key(
        self, map: MutMap[str, int], key: str, value: int
    ) -> None:
        map[key] = value
        assert map[key] == value

    # ==========test_get_or_set==========
    def test_get_or_set_should_return_corresponding_value_if_key_in_map(
        self, map: MutMap[str, int]
    ) -> None:
        assert map.get_or_set(1000, "a") == 1

    def test_get_or_set_should_not_overwrite_value_if_key_in_map(
        self, map: MutMap[str, int]
    ) -> None:
        map.get_or_set(1000, "a")
        assert map["a"] == 1

    def test_get_or_set_should_return_default_if_key_not_in_map(
        self, map: MutMap[str, int]
    ) -> None:
        assert map.get_or_set(1000, "z") == 1000

    def test_get_or_set_should_insert_default_if_key_not_in_map(
        self, map: MutMap[str, int]
    ) -> None:
        map.get_or_set(1000, "z")
        assert map["z"] == 1000

    # ==========test_get_or_else_set==========
    def test_get_or_else_set_should_return_corresponding_value_if_key_in_map(
        self, map: MutMap[str, int]
    ) -> None:
        assert map.get_or_else_set(lambda: 1000, "a") == 1

    def test_get_or_else_set_should_not_overwrite_value_if_key_in_map(
        self, map: MutMap[str, int]
    ) -> None:
        map.get_or_else_set(lambda: 1000, "a")
        assert map["a"] == 1

    def test_get_or_else_set_should_return_f_product_if_key_not_in_map(
        self, map: MutMap[str, int]
    ) -> None:
        assert map.get_or_else_set(lambda: 1000, "z") == 1000

    def test_get_or_else_set_should_insert_f_product_if_key_not_in_map(
        self, map: MutMap[str, int]
    ) -> None:
        map.get_or_else_set(lambda: 1000, "z")
        assert map["z"] == 1000

    def test_get_or_else_set_should_not_call_f_if_key_in_map(
        self, map: MutMap[str, int]
    ) -> None:
        f = mock.Mock()
        map.get_or_else_set(f, "a")
        f.assert_not_called()

    def test_get_or_else_set_should_call_f_if_key_not_in_map(
        self, map: MutMap[str, int]
    ) -> None:
        f = mock.Mock()
        map.get_or_else_set(f, "z")
        f.assert_called_once()


# ==========================================
# ===            Vectors                 ===
# ==========================================
class TestVec:
    @pytest.fixture
    def vec(self) -> Vec[str]:
        return Vec(["a", "b", "c"])

    # ==========test__init__==========
    def test__init__should_set_data_to_empty_sequence_if_not_provided(self) -> None:
        assert Vec[str]() == Vec[str]([])

    # ==========test__contains__==========
    @pytest.mark.parametrize(
        "value, expected",
        [
            ("a", True),
            ("b", True),
            ("c", True),
            ("d", False),
            ("z", False),
        ],
    )
    def test__contains__should_return_expected(
        self, vec: Vec[str], value: str, expected: bool
    ) -> None:
        assert (value in vec) is expected

    # ==========test__eq__==========
    @pytest.mark.parametrize(
        "value, expected",
        [
            (Vec(["a", "b", "c"]), True),
            (Vec(["a", "b", "c", "c"]), False),
            (Vec(["x", "y", "z"]), False),
            ("Hello world!", False),
            (100, False),
        ],
    )
    def test__eq__should_return_expected(
        self, vec: Vec[str], value: object, expected: bool
    ) -> None:
        assert (vec == value) is expected

    # ==========test__getitem__==========
    def test__getitem__should_return_value_if_idx_in_range(self, vec: Vec[str]) -> None:
        assert vec[0] == "a"

    def test__getitem__should_raise_index_error_if_idx_out_of_range(
        self, vec: Vec[str]
    ) -> None:
        with pytest.raises(IndexError):
            vec[100]

    # ==========test__iter__==========
    def test__iter__should_return_value_iterator(self, vec: Vec[str]) -> None:
        assert tuple(iter(vec)) == ("a", "b", "c")

    # ==========test__len__==========
    def test__len__should_return_length(self, vec: Vec[str]) -> None:
        assert len(vec) == 3

    # ==========test_first==========
    def test_first_should_return_some_containing_first_value_if_vec_not_empty(
        self, vec: Vec[str]
    ) -> None:
        assert vec.first() == Some("a")

    def test_first_should_return_nothing_if_vec_is_empty(self) -> None:
        assert Vec[str]().first() == Nothing()

    # ==========test_get==========
    @pytest.mark.parametrize(
        "idx, expected",
        [
            (0, Some("a")),
            (1, Some("b")),
            (2, Some("c")),
            (3, Nothing()),
            (100, Nothing()),
            (-1, Some("c")),
            (-2, Some("b")),
            (-3, Some("a")),
            (-4, Nothing()),
        ],
    )
    def test_get_should_return_expected(
        self, vec: Vec[str], idx: int, expected: Option[str]
    ) -> None:
        assert vec.get(idx) == expected

    def test_get_should_return_nothing_if_vec_is_empty(self) -> None:
        assert Vec[str]().get(0) == Nothing()

    # ==========test_get_or==========
    @pytest.mark.parametrize(
        "idx, expected",
        [
            (0, "a"),
            (1, "b"),
            (2, "c"),
            (3, "z"),
            (100, "z"),
            (-1, "c"),
            (-2, "b"),
            (-3, "a"),
            (-4, "z"),
        ],
    )
    def test_get_or_should_return_expected(
        self, vec: Vec[str], idx: int, expected: str
    ) -> None:
        assert vec.get_or("z", idx) == expected

    # ==========test_get_or_else==========
    @pytest.mark.parametrize(
        "idx, expected",
        [
            (0, "a"),
            (1, "b"),
            (2, "c"),
            (3, "z"),
            (100, "z"),
            (-1, "c"),
            (-2, "b"),
            (-3, "a"),
            (-4, "z"),
        ],
    )
    def test_get_or_else_should_return_expected(
        self, vec: Vec[str], idx: int, expected: str
    ) -> None:
        assert vec.get_or_else(lambda: "z", idx) == expected

    def test_get_or_else_should_not_call_f_if_idx_in_range(self, vec: Vec[str]) -> None:
        f = mock.Mock()
        vec.get_or_else(f, 0)
        f.assert_not_called()

    def test_get_or_else_should_call_f_if_idx_out_of_range(self, vec: Vec[str]) -> None:
        f = mock.Mock()
        vec.get_or_else(f, 100)
        f.assert_called_once()

    # ==========test_last==========
    def test_last_should_return_some_containing_last_value_if_vec_not_empty(
        self, vec: Vec[str]
    ) -> None:
        assert vec.last() == Some("c")

    def test_last_should_return_nothing_if_vec_is_empty(self) -> None:
        assert Vec[str]().last() == Nothing()


class TestMutVec:
    @pytest.fixture
    def vec(self) -> MutVec[str]:
        return MutVec(["a", "b", "c"])

    # ==========test__init__==========
    def test__init__should_set_data_to_empty_sequence_if_not_provided(self) -> None:
        assert MutVec[str]() == MutVec[str]([])

    # ==========test__setitem__==========
    def test__setitem__should_set_value_at_idx_if_idx_in_range(
        self, vec: MutVec[str]
    ) -> None:
        vec[0] = "z"
        assert vec[0] == "z"

    def test__setitem__should_raise_index_error_if_idx_out_of_range(
        self, vec: MutVec[str]
    ) -> None:
        with pytest.raises(IndexError):
            vec[100] = "z"

    # ==========test_append==========
    def test_append_should_insert_value_at_end_of_vec(self, vec: MutVec[str]) -> None:
        vec.append("z")
        assert vec[-1] == "z" and len(vec) == 4

    # ==========test_insert==========
    @pytest.mark.parametrize(
        "idx",
        [0, 1, 2],
    )
    def test_insert_should_insert_value_before_idx(
        self, vec: MutVec[str], idx: int
    ) -> None:
        vec.insert(idx, "z")
        assert vec[idx] == "z" and len(vec) == 4

    def test_insert_should_insert_value_at_end_of_vec_if_idx_ge_length(
        self, vec: MutVec[str]
    ) -> None:
        vec.insert(100, "z")
        assert vec[-1] == "z" and len(vec) == 4

    # ==========test_pop==========
    @pytest.mark.parametrize(
        "idx, expected",
        [
            (0, Some("a")),
            (1, Some("b")),
            (2, Some("c")),
            (3, Nothing()),
            (100, Nothing()),
            (-1, Some("c")),
            (-2, Some("b")),
            (-3, Some("a")),
            (-4, Nothing()),
        ],
    )
    def test_pop_should_return_expected(
        self, vec: MutVec[str], idx: int, expected: Option[str]
    ) -> None:
        assert vec.pop(idx) == expected

    @pytest.mark.parametrize(
        "idx, value",
        [(0, "a"), (1, "b"), (2, "c")],
    )
    def test_pop_should_remove_value_at_idx(
        self, vec: MutVec[str], idx: int, value: str
    ) -> None:
        vec.pop(idx)
        assert value not in vec and len(vec) == 2

    def test_pop_should_not_mutate_vec_if_idx_out_of_range(
        self, vec: MutVec[str]
    ) -> None:
        vec.pop(100)
        assert vec == Vec(["a", "b", "c"])

    # ==========test_pop_or==========
    @pytest.mark.parametrize(
        "idx, expected",
        [
            (0, "a"),
            (1, "b"),
            (2, "c"),
            (3, "z"),
            (100, "z"),
            (-1, "c"),
            (-2, "b"),
            (-3, "a"),
            (-4, "z"),
        ],
    )
    def test_pop_or_should_return_expected(
        self, vec: MutVec[str], idx: int, expected: str
    ) -> None:
        assert vec.pop_or("z", idx) == expected

    # ==========test_pop_or_else==========
    @pytest.mark.parametrize(
        "idx, expected",
        [
            (0, "a"),
            (1, "b"),
            (2, "c"),
            (3, "z"),
            (100, "z"),
            (-1, "c"),
            (-2, "b"),
            (-3, "a"),
            (-4, "z"),
        ],
    )
    def test_pop_or_else_should_return_expected(
        self, vec: MutVec[str], idx: int, expected: str
    ) -> None:
        assert vec.pop_or_else(lambda: "z", idx) == expected

    def test_pop_or_else_should_not_call_f_if_idx_in_range(
        self, vec: MutVec[str]
    ) -> None:
        f = mock.Mock()
        vec.pop_or_else(f, 0)
        f.assert_not_called()

    def test_pop_or_else_should_call_f_if_idx_out_of_range(
        self, vec: MutVec[str]
    ) -> None:
        f = mock.Mock()
        vec.pop_or_else(f, 100)
        f.assert_called_once()

    # ==========test_prepend==========
    def test_prepend_should_insert_value_at_start_of_vec(
        self, vec: MutVec[str]
    ) -> None:
        vec.prepend("z")
        assert vec[0] == "z" and len(vec) == 4
