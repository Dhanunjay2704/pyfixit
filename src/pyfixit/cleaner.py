from pathlib import Path

from pyfixit.requirements_parser import parse_requirement
from pyfixit.package_names import get_import_name


def clean_requirements(project_directory=".", apply=False):
    project_directory = Path(project_directory)

    requirements_file = project_directory / "requirements.txt"

    if not requirements_file.exists():
        return []

    lines = requirements_file.read_text(
        encoding="utf-8"
    ).splitlines()

    from pyfixit.imports import get_project_imports

    imports = get_project_imports(project_directory)

    kept = []
    removed = []

    for line in lines:

        original_line = line
        line = line.strip()

        if not line:
            kept.append(original_line)
            continue

        if line.startswith("#"):
            kept.append(original_line)
            continue

        parsed = parse_requirement(line)

        if parsed is None:
            kept.append(original_line)
            continue

        package_name = parsed["package"]

        import_name = get_import_name(package_name)

        if import_name not in imports:
            removed.append(original_line)
        else:
            kept.append(original_line)

    # Only modify requirements.txt when --apply is used
    if apply and removed:

        requirements_file.write_text(
            "\n".join(kept) + "\n",
            encoding="utf-8"
        )

    return removed