# Contributing to Azure Agent Starter Pack

Thank you for your interest in contributing to the Azure Agent Starter Pack! We welcome contributions from the community to help make this tool better for everyone.

## Code of Conduct

By participating in this project, you agree to abide by our [Code of Conduct](CODE_OF_CONDUCT.md).

## How to Contribute

1.  **Report Bugs**: If you find a bug, please open an issue on GitHub with a detailed description and steps to reproduce.
2.  **Suggest Features**: Have an idea for a new feature? Open an issue to discuss it.
3.  **Submit Pull Requests**:
    *   Fork the repository.
    *   Create a new branch for your changes (`git checkout -b feature/your-feature`).
    *   Make your changes and ensure they follow the project's coding standards.
    *   Add tests for any new functionality.
    *   Submit a pull request with a clear description of your changes.

## Development Setup

We use `uv` for dependency management and packaging.

1.  Clone the repository:
    ```bash
    git clone https://github.com/nkamrudeen/azure-agent-starter-pack.git
    cd azure-agent-starter-pack
    ```
2.  Sync dependencies:
    ```bash
    uv sync
    ```
3.  Install as an editable tool for easier testing:
    ```bash
    uv tool install --from . --editable azure-agent-starter-pack
    ```

## Coding Standards

*   We use `ruff` for linting and formatting. Run `ruff check` and `ruff format` before submitting a PR.
*   Write clear, concise commit messages.
*   Ensure all tests pass by running `pytest`.
