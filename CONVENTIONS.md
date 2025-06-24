Use Python 3.13

Do not write code specifically to handle backwards compatibility with older versions of Python. Only support Python 3.13, and simplify any code that can be simplified with modern Python features.

Do not use `from future import ...` syntax. Only use features available in Python 3.13.

Use Pydantic 2. Do not use Pydantic 1. Certain important methods changed from Pydantic 1 to 2, so make sure you don't use any deprecated methods.

Use modern type annotations. Do not use the `typing` module unless you have to. Instead of `Optional[str]` use `str | None`, etc.

Do not write docstrings except at the top of modules.
All modules should have a docstring.
Ensure that module docstrings are dense and useful. Do not simply restate the methods and the code, but rather explain what it does at a high level, as context for the developer.
Do not write function docstrings, do not write module docstrings, do not write class docstrings.

Do not write comments unless they specifically call attention to something that the code does not communicate itself. Otherwise do not write comments that simply restate what the code is doing.


## What's Been Simplified in Python 3.13+ Type Hints

1. **Union Types**: Use `X | Y` instead of `Union[X, Y]`
2. **Optional Types**: Use `X | None` instead of `Optional[X]`
3. **Collection Types**: Use `list[X]`, `dict[X, Y]`, etc. instead of `List[X]`, `Dict[X, Y]`
4. **Type Aliases**: Use simple assignment (`type URL = str`) instead of `TypeAlias`
