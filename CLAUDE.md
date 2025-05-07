# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands
- Run data processing: `python process.py`
- Validate data: `python validate.py`
- Format code: `black .`
- Lint code: `flake8`
- Run tests: `pytest`
- Run single test: `pytest tests/test_file.py::test_function`

## Code Guidelines
- Use Python 3.8+ features
- Organize imports alphabetically: stdlib, third-party, local
- Use type hints for all function parameters and return values
- Use snake_case for variables/functions, CamelCase for classes
- Prefer pandas for Excel processing
- Handle exceptions with specific error types
- Document functions with docstrings
- Log operations that modify data
- Keep functions short (< 50 lines)
- Use descriptive variable names related to the sport/league context