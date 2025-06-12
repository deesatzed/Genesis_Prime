# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Build & Test Commands
- Run all tests: `python tests/run_tests.py`
- Run single test: `python tests/run_tests.py tests/path/to/test_file.py::test_function -v`
- Run tests in directory: `python tests/run_tests.py tests/directory_name`
- Install package for development: `pip install -e .`

## Code Style Guidelines
- **Formatting**: PEP 8, 4-space indentation
- **Imports**: Group by standard library, third-party, local (alphabetically within groups)
- **Types**: Use typing annotations for parameters and return values
- **Naming**: Classes: PascalCase, Functions/Variables: snake_case, Constants: UPPER_SNAKE_CASE
- **Error Handling**: Use custom exceptions derived from ServiceException, log errors appropriately
- **Documentation**: Google-style docstrings with Args, Returns, Raises sections
- **Architecture**: Modular design with APIs, controllers, and services layers
- **Testing**: pytest framework with pytest-asyncio for async tests
- **Directory Structure**: Hyphenated-lowercase for services, snake_case for code modules