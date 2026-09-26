# PyFixIt

[![PyPI](https://img.shields.io/pypi/v/pyfixit-cli.svg)](https://pypi.org/project/pyfixit-cli/)
[![Python](https://img.shields.io/pypi/pyversions/pyfixit-cli.svg)](https://pypi.org/project/pyfixit-cli/)
[![License](https://img.shields.io/pypi/l/pyfixit-cli.svg)](https://github.com/Dhanunjay2704/pyfixit/blob/main/LICENSE)

### Python Project Troubleshooter

PyFixIt is a command-line tool that analyzes Python projects and diagnoses common import and dependency problems.

It can detect:

- Missing dependencies
- Undeclared dependencies
- Version conflicts
- Unused dependencies
- Standard-library modules
- Local project modules
- Package-name differences such as `sklearn -> scikit-learn`

---

## Features

### Dependency Diagnosis

PyFixIt analyzes Python files in a project and compares the detected imports with `requirements.txt`.

Example:

```text
[PROBLEM] sklearn

  Status: missing_installation

  Fix: pip install scikit-learn
```

---

### Version Conflict Detection

PyFixIt checks installed versions against the versions specified in `requirements.txt`.

Example:

```text
[VERSION CONFLICT] requests

  Required: ==2.30.0

  Installed: 2.34.2

  Fix: pip install requests==2.30.0
```

---

### Missing Declaration Detection

If a package is installed and imported but not declared in `requirements.txt`, PyFixIt reports it.

Example:

```text
[PROBLEM] pandas

  Status: missing_declaration

  Fix: Add 'pandas' to requirements.txt
```

---

### Unused Dependency Detection

PyFixIt can identify packages listed in `requirements.txt` that are not imported by the project.

Example:

```text
[UNUSED] numpy

  Fix: Remove 'numpy' from requirements.txt
```

---

### Requirements Cleanup

You can preview unused dependencies:

```bash
pyfixit clean .
```

Then apply the cleanup:

```bash
pyfixit clean . --apply
```

---

## Installation

### From Source

Clone the repository:

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
```

Navigate into the project:

```bash
cd pyfixit
```

Create a virtual environment:

```bash
python -m venv .venv
```

### Windows

Activate the virtual environment:

```bash
.venv\Scripts\activate
```

### Linux / macOS

Activate the virtual environment:

```bash
source .venv/bin/activate
```

Install PyFixIt in editable mode:

```bash
python -m pip install -e .
```

---

## Usage

### Diagnose a Project

Run:

```bash
pyfixit diagnose .
```

Example output:

```text
PyFixIt v0.1.0
Python Project Troubleshooter

Dependencies
------------------------------

[PROBLEM] sklearn

  Status: missing_installation

  Fix: pip install scikit-learn

[VERSION CONFLICT] requests

  Required: ==2.30.0

  Installed: 2.34.2

  Fix: pip install requests==2.30.0

[PROBLEM] pandas

  Status: missing_declaration

  Fix: Add 'pandas' to requirements.txt


Unused dependencies
------------------------------

[UNUSED] numpy

  Fix: Remove 'numpy' from requirements.txt
```

You can also use the shorthand:

```bash
pyfixit .
```

---

## Check a Project

The `check` command provides a quick project health summary.

Run:

```bash
pyfixit check .
```

Example:

```text
PyFixIt v0.1.0
Python Project Troubleshooter

Checking project...

[FAIL] 4 dependency problems found

[OK] No unused dependencies found
```

For a clean project:

```text
PyFixIt v0.1.0
Python Project Troubleshooter

Checking project...

[OK] No dependency problems found

[OK] No unused dependencies found
```

PyFixIt also uses exit codes, so it can be used in scripts and CI pipelines.

---

## JSON Output

For machine-readable diagnosis results:

```bash
pyfixit diagnose . --json
```

Example:

```json
{
  "dependencies": [
    {
      "module": "sklearn",
      "package_name": "scikit-learn",
      "import_name": "sklearn",
      "declared": true,
      "installed": false,
      "installed_version": null,
      "required_version": null,
      "operator": null,
      "status": "missing_installation"
    }
  ],
  "unused_dependencies": [
    "numpy"
  ]
}
```

JSON output can be useful for automation, CI tools, and other developer tooling.

---

## Clean Requirements

PyFixIt can identify unused dependencies and optionally remove them from `requirements.txt`.

### Preview Unused Dependencies

Run:

```bash
pyfixit clean .
```

Example:

```text
Cleaning requirements.txt
------------------------------

[REMOVE] numpy

1 unused dependencies found.

Run 'pyfixit clean . --apply' to remove them.
```

### Apply the Cleanup

Run:

```bash
pyfixit clean . --apply
```

Example:

```text
Cleaning requirements.txt
------------------------------

[REMOVED] numpy

1 dependencies removed.
```

Running the command again will show:

```text
Cleaning requirements.txt
------------------------------

Nothing to remove.
```

---

## Available Commands

| Command | Description |
|---|---|
| `pyfixit diagnose .` | Diagnose project dependencies |
| `pyfixit check .` | Quickly check project health |
| `pyfixit clean .` | Preview unused dependencies |
| `pyfixit clean . --apply` | Remove unused dependencies |
| `pyfixit diagnose . --json` | Output diagnosis as JSON |
| `pyfixit --help` | Show help |
| `pyfixit --version` | Show version |

---

## What PyFixIt Checks

PyFixIt analyzes imports and classifies them into three categories:

```text
Standard Library
|
+-- pathlib
+-- sys
+-- ast

Local Modules
|
+-- project files
+-- project packages

Third-Party Modules
|
+-- requests
+-- pandas
+-- fastapi
+-- sklearn
```

Only third-party modules are checked against project dependencies.

This prevents standard-library and local project modules from being incorrectly reported as missing dependencies.

---

## Package Name Mapping

Some Python import names are different from their package names.

For example:

```python
import sklearn
```

The package is installed using:

```bash
pip install scikit-learn
```

PyFixIt handles this distinction automatically.

```text
Import name:  sklearn

Package name: scikit-learn
```

This allows PyFixIt to provide more accurate installation suggestions.

---

## Requirements

PyFixIt currently requires:

- Python 3.10+
- `packaging >= 22`

---

## Development

Clone the repository and install it in editable mode:

```bash
python -m pip install -e .
```

Install pytest:

```bash
python -m pip install pytest
```

Run the test suite:

```bash
python -m pytest
```

### Test Status

Current test suite:

```text
47 passed
```

---

## Project Structure

```text
pyfixit/
|
+-- src/
|   +-- pyfixit/
|       +-- __init__.py
|       +-- cleaner.py
|       +-- cli.py
|       +-- dependencies.py
|       +-- diagnostics.py
|       +-- environment.py
|       +-- imports.py
|       +-- module_classifier.py
|       +-- package_mapping.py
|       +-- package_names.py
|       +-- requirements_parser.py
|
+-- tests/
|   +-- test_cleaner.py
|   +-- test_cli.py
|   +-- test_diagnostics.py
|   +-- test_package_names.py
|   +-- test_requirements_parser.py
|
+-- pyproject.toml
+-- README.md
+-- requirements.txt
```

---

## Version

**Current version: `0.1.0`**

PyFixIt is currently in its initial release.

---

## License

This project is licensed under the MIT License.