import sys
from pathlib import Path


def is_standard_library(module_name):
    if module_name in sys.stdlib_module_names:
        return True

    return False


def is_local_module(module_name, project_directory="."):
    project_directory = Path(project_directory)

    possible_locations = [
        project_directory,
        project_directory / "src"
    ]

    for location in possible_locations:

        module_file = location / f"{module_name}.py"
        module_directory = location / module_name

        if module_file.exists():
            return True

        if module_directory.is_dir():
            init_file = module_directory / "__init__.py"

            if init_file.exists():
                return True

    return False


def classify_module(module_name, project_directory="."):
    if is_standard_library(module_name):
        return "standard_library"

    if is_local_module(module_name, project_directory):
        return "local"

    return "third_party"


def classify_modules(modules, project_directory="."):
    classified = {
        "standard_library": [],
        "local": [],
        "third_party": []
    }

    for module in modules:
        category = classify_module(module, project_directory)

        if module not in classified[category]:
            classified[category].append(module)

    return classified


