# Python Best Practices

A comprehensive guide to writing high-quality Python code, from style conventions to project structure.

## Overview

This document compiles Python-specific best practices covering code style, project organization, tooling, and modern development workflows.

---

## Python Code Style Guide

**Source:** [The Hitchhiker's Guide to Python - Style Guide](https://docs.python-guide.org/writing/style/)

### Core Philosophy

Python's design emphasizes readability and explicit code. The community follows established conventions to make code accessible and maintainable across projects.

### General Principles

**Explicit Over Implicit**: Code should clearly express intent. Use straightforward function signatures and direct return statements rather than relying on unpacking tricks or magic.

**One Statement Per Line**: Avoid combining multiple operations on a single line, except for concise list comprehensions. This improves clarity and debugging.

**Function Arguments**: Use positional arguments for essential parameters, keyword arguments with defaults for optional settings. Avoid `*args` and `**kwargs` unless truly necessary, as they reduce clarity about what the function accepts.

**Avoiding Complexity**: Python offers powerful metaprogramming capabilities, but these should be used sparingly. Readability trumps cleverness—"A Pythonista knows how to kill with a single finger, and never to actually do it."

**Responsibility Culture**: Python has no private keyword. Instead, the community uses underscore prefixes (`_variable`) to indicate internal implementation details that shouldn't be accessed directly.

---

## Common Python Idioms

### Unpacking
Assign tuple elements to variables efficiently:
```python
# Swapping variables
a, b = b, a

# Multiple return values
def get_coordinates():
    return 10, 20

x, y = get_coordinates()
```

### Throwaway Variables
Use `_` for unused assignments:
```python
for _ in range(10):
    print("Hello")

# Unpacking with ignored values
first, *_, last = [1, 2, 3, 4, 5]
```

### String Operations
```python
# Joining strings (preferred)
result = ''.join(['hello', ' ', 'world'])

# String formatting (modern)
name = "Alice"
greeting = f"Hello, {name}!"  # f-strings (Python 3.6+)
```

### Collections
Use the right data structure:
```python
# Sets for membership testing
allowed_users = {'alice', 'bob', 'charlie'}
if user in allowed_users:  # O(1) lookup
    grant_access()

# Dictionaries for key-value pairs
config = {'host': 'localhost', 'port': 8080}
```

---

## PEP 8 and Style Enforcement

### PEP 8 Overview

**PEP 8** is the official Python style guide. Key points:

- **Indentation**: 4 spaces (not tabs)
- **Line Length**: Maximum 79 characters
- **Blank Lines**: 2 between top-level definitions, 1 between methods
- **Imports**: One per line, grouped (standard lib, third-party, local)
- **Naming Conventions**:
  - `snake_case` for functions and variables
  - `PascalCase` for classes
  - `UPPER_CASE` for constants
  - `_leading_underscore` for internal use

### Style Checking Tools

**pycodestyle** (formerly pep8): Checks compliance with PEP 8
```bash
pycodestyle myfile.py
```

**autopep8**: Automatically fixes PEP 8 violations
```bash
autopep8 --in-place --aggressive myfile.py
```

**yapf**: Google's Python formatter
```bash
yapf --in-place myfile.py
```

**black**: Opinionated, uncompromising formatter
```bash
black myfile.py
```

---

## Pythonic Practices

### Implicit Truthiness
```python
# Good
if items:
    process(items)

# Avoid
if items != []:
    process(items)
```

### Dictionary Operations
```python
# Safe dictionary access
value = config.get('key', default_value)

# Membership testing
if 'key' in config:
    use(config['key'])

# Dictionary comprehensions
squares = {x: x**2 for x in range(10)}
```

### List Comprehensions
```python
# Good
evens = [x for x in range(10) if x % 2 == 0]

# Avoid nested loops in comprehensions (use nested for loops instead)
# Good
result = []
for x in matrix:
    for y in x:
        result.append(y)
```

### Context Managers
```python
# Always use 'with' for file operations
with open('file.txt', 'r') as f:
    content = f.read()

# Multiple context managers
with open('input.txt') as infile, open('output.txt', 'w') as outfile:
    outfile.write(infile.read())
```

### Line Continuation
```python
# Use parentheses (preferred)
result = (
    some_function(arg1, arg2)
    + another_function(arg3)
)

# Avoid backslashes
result = some_function(arg1, arg2) \
    + another_function(arg3)  # Not preferred
```

---

## Python Package Template

**Source:** [Python Package Template by TezRomacH](https://github.com/TezRomacH/python-package-template)

This cookiecutter template demonstrates modern Python development standards by integrating essential tools and workflows.

### Development Tools

The template leverages **code quality and formatting tools**:
- **Black**: Uncompromising code formatter
- **isort**: Import statement organizer
- **pyupgrade**: Automatic syntax upgrades to newer Python versions
- **MyPy**: Static type checking
- **Pytest**: Testing framework
- **Darglint**: Docstring validation
- **Safety**: Security vulnerability scanning
- **Bandit**: Security issue detection

Pre-commit hooks automate these checks before commits, ensuring code meets standards before reaching the repository.

### Project Structure

**Poetry manages dependencies** through `pyproject.toml` and `setup.cfg`, supporting Python 3.7+. The template provides well-configured configuration files including `.editorconfig`, `.gitignore`, and `.dockerignore`.

Typical structure:
```
my_package/
├── .github/
│   └── workflows/          # CI/CD pipelines
├── docs/                   # Documentation
├── my_package/            # Source code
│   ├── __init__.py
│   └── module.py
├── tests/                 # Test files
│   ├── __init__.py
│   └── test_module.py
├── .editorconfig
├── .gitignore
├── .pre-commit-config.yaml
├── pyproject.toml         # Project metadata and dependencies
├── setup.cfg              # Tool configurations
├── README.md
├── LICENSE
└── CONTRIBUTING.md
```

### CI/CD & Automation

GitHub Actions powers the build pipeline with predefined workflows. **"Automatic drafts of new releases with Release Drafter"** organize pull request changes by labels, following Semantic Versioning.

The Stale bot automatically manages inactive issues, while Dependabot keeps dependencies current.

### Community Standards

The template auto-generates governance files:
- **LICENSE**: Project licensing
- **CONTRIBUTING.md**: Contribution guidelines
- **CODE_OF_CONDUCT.md**: Community standards
- **SECURITY.md**: Security policy

Pull request and issue templates guide contributor interactions.

### Deployment

Docker support and Makefile automation streamline builds, testing, and deployment tasks. This comprehensive approach reduces setup friction while establishing professional development practices across new projects.

---

## Modern Python Tooling

### Dependency Management

**Poetry** (Recommended for modern projects):
```bash
# Initialize new project
poetry new my-project

# Add dependencies
poetry add requests

# Add dev dependencies
poetry add --dev pytest

# Install dependencies
poetry install

# Run commands in virtual environment
poetry run python script.py
```

**pip** with **requirements.txt**:
```bash
# Install from requirements file
pip install -r requirements.txt

# Generate requirements
pip freeze > requirements.txt
```

**pip-tools** for deterministic builds:
```bash
# requirements.in
requests
flask>=2.0

# Compile to requirements.txt
pip-compile requirements.in
```

### Type Checking

**mypy** for static type analysis:
```python
# Type hints
def greet(name: str) -> str:
    return f"Hello, {name}!"

# Type checking collections
from typing import List, Dict, Optional

def process_items(items: List[str]) -> Dict[str, int]:
    return {item: len(item) for item in items}

# Optional types
def find_user(user_id: int) -> Optional[User]:
    return users.get(user_id)
```

### Linting

**flake8** combines multiple tools:
```bash
flake8 my_package/
```

**pylint** for comprehensive analysis:
```bash
pylint my_package/
```

**ruff** - Fast Python linter (modern alternative):
```bash
ruff check my_package/
```

### Testing

**pytest** - Modern testing framework:
```python
# test_calculator.py
def test_addition():
    assert 1 + 1 == 2

def test_division():
    assert 10 / 2 == 5

# Fixtures
import pytest

@pytest.fixture
def sample_data():
    return [1, 2, 3, 4, 5]

def test_sum(sample_data):
    assert sum(sample_data) == 15
```

### Documentation

**Sphinx** for documentation generation:
```bash
# Initialize Sphinx
sphinx-quickstart docs/

# Build documentation
cd docs/
make html
```

**MkDocs** for Markdown-based docs:
```bash
# Install
pip install mkdocs

# Create project
mkdocs new my-project

# Serve locally
mkdocs serve

# Build static site
mkdocs build
```

---

## Configuration Files

### pyproject.toml

Modern Python configuration standard (PEP 518):
```toml
[tool.poetry]
name = "my-package"
version = "0.1.0"
description = "A sample package"
authors = ["Your Name <you@example.com>"]

[tool.poetry.dependencies]
python = "^3.8"
requests = "^2.28.0"

[tool.poetry.dev-dependencies]
pytest = "^7.0"
black = "^22.0"
mypy = "^0.950"

[tool.black]
line-length = 100
target-version = ['py38']

[tool.isort]
profile = "black"
line_length = 100

[tool.mypy]
python_version = "3.8"
warn_return_any = true
warn_unused_configs = true
```

### setup.cfg

Traditional configuration file:
```ini
[flake8]
max-line-length = 100
exclude = .git,__pycache__,build,dist

[mypy]
python_version = 3.8
warn_return_any = True
warn_unused_configs = True

[tool:pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
```

### .pre-commit-config.yaml

Automate checks before commits:
```yaml
repos:
  - repo: https://github.com/psf/black
    rev: 22.10.0
    hooks:
      - id: black
        language_version: python3.8

  - repo: https://github.com/pycqa/isort
    rev: 5.10.1
    hooks:
      - id: isort

  - repo: https://github.com/pycqa/flake8
    rev: 5.0.4
    hooks:
      - id: flake8

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v0.990
    hooks:
      - id: mypy
```

---

## Best Practices Summary

### Code Quality
1. **Follow PEP 8**: Use automated formatters like Black
2. **Type Hints**: Add type annotations for better IDE support and error detection
3. **Docstrings**: Document all public functions, classes, and modules
4. **Keep it Simple**: Prefer readability over cleverness
5. **DRY Principle**: Don't Repeat Yourself

### Project Structure
1. **Logical Organization**: Group related functionality
2. **Clear Naming**: Use descriptive names for modules and packages
3. **Separation of Concerns**: Keep business logic separate from infrastructure
4. **Configuration Files**: Use modern tools like pyproject.toml
5. **Tests Alongside Code**: Mirror source structure in tests

### Development Workflow
1. **Virtual Environments**: Always use isolated environments
2. **Version Control**: Commit early and often
3. **Pre-commit Hooks**: Catch issues before they reach the repository
4. **Continuous Integration**: Run tests on every commit
5. **Dependency Pinning**: Lock dependency versions for reproducibility

### Documentation
1. **README First**: Write documentation as you code
2. **API Documentation**: Use docstrings for automatic generation
3. **Examples**: Include usage examples
4. **Changelog**: Maintain a history of changes
5. **Type Hints**: They serve as inline documentation

### Security
1. **Dependency Scanning**: Use tools like Safety and Bandit
2. **Secret Management**: Never commit credentials
3. **Input Validation**: Validate and sanitize all inputs
4. **Regular Updates**: Keep dependencies current
5. **Security Policies**: Document vulnerability reporting process

---

## Common Anti-Patterns to Avoid

### Code Smells
- **God Classes**: Classes that do too much
- **Long Functions**: Functions exceeding 20-30 lines
- **Deep Nesting**: More than 3-4 levels of indentation
- **Magic Numbers**: Unexplained constants in code
- **Mutable Defaults**: Using mutable objects as default arguments

### Bad Practices
```python
# DON'T: Mutable default arguments
def add_item(item, items=[]):  # Bug: list is shared across calls
    items.append(item)
    return items

# DO: Use None as default
def add_item(item, items=None):
    if items is None:
        items = []
    items.append(item)
    return items

# DON'T: Bare except
try:
    risky_operation()
except:  # Catches everything, including KeyboardInterrupt
    pass

# DO: Catch specific exceptions
try:
    risky_operation()
except ValueError as e:
    log.error(f"Invalid value: {e}")

# DON'T: String concatenation in loops
result = ""
for item in items:
    result += str(item)  # Creates new string each iteration

# DO: Use join
result = "".join(str(item) for item in items)
```

---

## Resources and Further Reading

### Official Documentation
- [Python Documentation](https://docs.python.org/)
- [PEP 8 Style Guide](https://pep8.org/)
- [The Python Tutorial](https://docs.python.org/3/tutorial/)

### Books
- "Fluent Python" by Luciano Ramalho
- "Effective Python" by Brett Slatkin
- "Python Tricks" by Dan Bader

### Online Resources
- [Real Python](https://realpython.com/)
- [Python Package Index (PyPI)](https://pypi.org/)
- [Awesome Python](https://github.com/vinta/awesome-python)

### Tools
- [Black](https://black.readthedocs.io/)
- [Poetry](https://python-poetry.org/)
- [pytest](https://docs.pytest.org/)
- [mypy](http://mypy-lang.org/)
- [Sphinx](https://www.sphinx-doc.org/)
