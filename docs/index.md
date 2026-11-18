# Bento

Bento is the all-in-one toolkit for Python. It aims to take the existing features of Python and extend them without adding extra dependencies.

Current features:

- **Maps**: dictionary-like objects that expose methods allowing for chainable operations
- **Monads**: the `Option` and `Result` types provide a more explicit way to handle missing values or errors
- **Vectors**: resizable sequences that expose methods allowing for chainable operations

Upcoming features:

- **Async**: a package that will provide wrappers for monads to chain async operations
- **HTTP**: an ASGI compliant web micro-framework intended to be used for simple web services or as a building block for larger web frameworks

For the complete source code visit https://github.com/Romeyus/bento.

## Installation

We recommend [installing uv](https://docs.astral.sh/uv/getting-started/installation) first, then add Bento to your project.

```bash
uv add bento
```

You can also create a virtual environment and add Bento to your project with `pip install bento`.

## License

This project is licensed under the terms of the MIT license.
