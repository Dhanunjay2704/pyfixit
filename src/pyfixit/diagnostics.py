import importlib.util
from importlib.metadata import version, PackageNotFoundError
from pathlib import Path

from pyfixit.package_names import get_import_name, get_package_name
from pyfixit.requirements_parser import parse_requirement, check_version


def check_dependency_declared(package_name, dependencies):
    for dependency in dependencies:

        parsed = parse_requirement(dependency)

        if parsed is None:
            continue

        if parsed["package"].lower() == package_name.lower():
            return True

    return False


def check_dependency_installed(module_name):
    try:
        spec = importlib.util.find_spec(module_name)

        if spec is None:
            return False

        return True

    except ModuleNotFoundError:
        return False


def get_installed_version(package_name):
    try:
        return version(package_name)

    except PackageNotFoundError:
        return None


def diagnose_dependency(module_name, dependencies):

    import_name = module_name
    package_name = get_package_name(module_name)

    declared = False
    required_version = None
    operator = None

    for dependency in dependencies:

        parsed = parse_requirement(dependency)

        if parsed is None:
            continue

        declared_package = parsed["package"]

        if declared_package.lower() == package_name.lower():

            declared = True
            required_version = parsed["version"]
            operator = parsed["operator"]

            break

    installed = check_dependency_installed(
        import_name
    )

    installed_version = None

    if installed:
        installed_version = get_installed_version(
            package_name
        )

    if not declared and not installed:

        status = "missing_declaration_and_installation"

    elif declared and not installed:

        status = "missing_installation"

    elif not declared and installed:

        status = "missing_declaration"

    elif required_version is not None:

        if check_version(
            installed_version,
            operator,
            required_version
        ):

            status = "ok"

        else:

            status = "version_conflict"

    else:

        status = "ok"

    return {
        "module": module_name,
        "package_name": package_name,
        "import_name": import_name,
        "declared": declared,
        "installed": installed,
        "installed_version": installed_version,
        "required_version": required_version,
        "operator": operator,
        "status": status
    }


def diagnose_dependencies(modules, dependencies):

    results = []

    for module in modules:

        result = diagnose_dependency(
            module,
            dependencies
        )

        results.append(result)

    return results


def read_requirements(project_directory="."):

    requirements_file = Path(
        project_directory
    ) / "requirements.txt"

    if not requirements_file.exists():
        return []

    dependencies = []

    with open(
        requirements_file,
        "r",
        encoding="utf-8"
    ) as file:

        for line in file:

            line = line.strip()

            if not line:
                continue

            if line.startswith("#"):
                continue

            dependencies.append(line)

    return dependencies


def find_unused_dependencies(imports, dependencies):

    unused = []

    for dependency in dependencies:

        parsed = parse_requirement(dependency)

        if parsed is None:
            continue

        package_name = parsed["package"]

        import_name = get_import_name(
            package_name
        )

        if import_name not in imports:

            unused.append(dependency)

    return unused


def diagnose_project(project_directory="."):

    from pyfixit.imports import get_project_imports
    from pyfixit.module_classifier import classify_modules

    imports = get_project_imports(
        project_directory
    )

    classified = classify_modules(
        imports,
        project_directory
    )

    declared_dependencies = read_requirements(
        project_directory
    )

    third_party_modules = classified[
        "third_party"
    ]

    results = diagnose_dependencies(
        third_party_modules,
        declared_dependencies
    )

    unused_dependencies = find_unused_dependencies(
        imports,
        declared_dependencies
    )

    return {
        "dependencies": results,
        "unused_dependencies": unused_dependencies
    }


def get_fix_suggestion(result):

    status = result["status"]

    module = result["module"]

    package_name = result.get(
        "package_name",
        module
    )

    if status == "missing_installation":

        return f"pip install {package_name}"

    if status == "missing_declaration_and_installation":

        return (
            f"Install it with: pip install {package_name}\n"
            f"Then add '{package_name}' to requirements.txt"
        )

    if status == "missing_declaration":

        return (
            f"Add '{package_name}' to requirements.txt"
        )

    if status == "version_conflict":

        required_version = result["required_version"]
        operator = result["operator"]

        return (
            f"pip install "
            f"{package_name}{operator}{required_version}"
        )

    if status == "ok":

        return "No action needed"

    return "No fix available"



def get_diagnosis_summary(diagnosis):
    dependencies = diagnosis["dependencies"]
    unused_dependencies = diagnosis["unused_dependencies"]

    problems = 0

    for dependency in dependencies:
        if dependency["status"] != "ok":
            problems += 1

    return {
        "total_dependencies": len(dependencies),
        "problems": problems,
        "unused_dependencies": len(unused_dependencies)
    }