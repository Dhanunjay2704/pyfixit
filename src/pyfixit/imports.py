import ast
from pathlib import Path


EXCLUDED_DIRECTORIES = {
    ".venv",
    "venv",
    "env",
    "test_env",
    "__pycache__",
    ".git",
    "site-packages",
    "build",
    "dist",
    ".pytest_cache",
    "tests",
}


def find_python_files(project_directory):
    project_path = Path(project_directory).resolve()

    python_files = []

    for path in project_path.rglob("*.py"):
        path = path.resolve()

        if any(part in EXCLUDED_DIRECTORIES for part in path.parts):
            continue

        # Don't analyze PyFixIt's own source code
        if "src" in path.parts and "pyfixit" in path.parts:
            continue

        python_files.append(path)

    return python_files


def get_imports_from_file(file_path):
    imports = []

    try:
        source = Path(file_path).read_text(
            encoding="utf-8"
        )

        tree = ast.parse(source)

    except (SyntaxError, UnicodeDecodeError):
        return imports

    for node in ast.walk(tree):

        if isinstance(node, ast.Import):

            for alias in node.names:

                module = alias.name.split(".")[0]

                if module not in imports:
                    imports.append(module)

        elif isinstance(node, ast.ImportFrom):

            if node.module is not None:

                module = node.module.split(".")[0]

                if module not in imports:
                    imports.append(module)

    return imports


def get_project_imports(project_directory="."):

    python_files = find_python_files(
        project_directory
    )

    all_imports = []

    for file_path in python_files:

        imports = get_imports_from_file(
            file_path
        )

        for module in imports:

            if module not in all_imports:
                all_imports.append(module)

    return all_imports