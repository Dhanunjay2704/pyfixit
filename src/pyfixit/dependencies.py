from pathlib import Path
from importlib.metadata import version, PackageNotFoundError


def find_requirements_file():
    requirements_file = Path("requirements.txt")

    if requirements_file.exists():
        return requirements_file

    return None


def read_requirements(requirements_file):
    dependencies = []

    with open(requirements_file, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()

            if line and not line.startswith("#"):
                dependencies.append(line)

    return dependencies


def is_package_installed(package_name):
    try:
        version(package_name)
        return True
    except PackageNotFoundError:
        return False