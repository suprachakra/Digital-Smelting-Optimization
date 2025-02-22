## Test Coverage Reports

This folder contains generated coverage reports from the continuous integration (CI) pipeline.

### Structure

- `coverage.xml` or `coverage.json`: Machine-readable coverage data for external tools (e.g., Codecov).
- `htmlcov/`: (Optional) HTML-based coverage reports for human-friendly viewing.
- `coverage_summary.txt`: A text-based summary of coverage percentages across modules.

### Usage

1. **CI/CD Generation**: The pipeline automatically generates coverage data when you run `pytest --cov`.
2. **Viewing Reports**:
   - If HTML reports are generated, open `htmlcov/index.html` in your browser.
   - If using Codecov or similar, the coverage data is uploaded automatically.
3. **Maintenance**: You can add these artifacts to `.gitignore` if they become large. For demonstration, they’re stored here for easy reference.
