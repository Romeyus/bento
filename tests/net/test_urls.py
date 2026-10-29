import pytest

from bento import net


class TestPath:
    def test_path_should_return_slash_if_value_is_empty_string(self) -> None:
        assert net.Path("") == "/"

    @pytest.mark.parametrize(
        "value, expected",
        [
            ["/hello/", "/hello"],
            ["hello/", "/hello"],
            ["/hello/world/", "/hello/world"],
            ["hello/world/", "/hello/world"],
        ],
    )
    def test_path_should_remove_trailing_slash(self, value: str, expected: str) -> None:
        assert net.Path(value) == expected

    @pytest.mark.parametrize(
        "value, expected",
        [
            ["//hello", "/hello"],
            ["hello//", "/hello"],
            ["//hello//", "/hello"],
            ["hello//world", "/hello/world"],
            ["//hello///world//", "/hello/world"],
        ],
    )
    def test_path_should_remove_duplicate_slashes(
        self, value: str, expected: str
    ) -> None:
        assert net.Path(value) == expected
