### Contributing to the Digital Smelting Optimization Project

Thank you for your interest in contributing! We welcome all kinds of contributions, including bug fixes, new features, documentation improvements, and more.

#### Getting Started

1. **Fork the repository** and clone it locally.
2. **Set up your environment**:
   - Install dependencies: `pip install -r requirements.txt`
   - (Optional) Build Docker image for consistent environment: `docker build -t metalx-optimizer .`
3. **Create a new branch** for your work: `git checkout -b feature/my-new-feature`

#### Code Guidelines

- Follow [PEP 8](https://peps.python.org/pep-0008/) style guidelines for Python code.
- Write **docstrings** for all public functions/classes.
- Use Python’s **logging** instead of `print` statements.

#### Testing

- Run `pytest` in the project root to execute all tests.
- Add new tests in the `tests/` folder if you fix a bug or add a feature.
- Ensure coverage does not drop below 80%.

#### Pull Requests

1. **Rebase** your branch onto `main` to avoid merge conflicts.
2. **Open a PR** with a descriptive title and link any related issues.
3. **Address review comments** promptly.

#### Reporting Issues

- Use the [GitHub Issues](../issues) to report bugs or request features.
- Include as much detail as possible (OS, steps to reproduce, logs, etc.).

We appreciate your contributions!
