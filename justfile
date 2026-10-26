check:
    @uv run basedpyright
    @uv run ruff check

test:
    @uv run pytest
