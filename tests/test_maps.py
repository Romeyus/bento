from unittest import mock

import pytest

from bento import Map, MutMap, Nothing, Option, Some


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
