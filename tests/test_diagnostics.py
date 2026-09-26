
from unittest.mock import patch
from pyfixit.diagnostics import (
    check_dependency_declared,
    diagnose_dependency,
    get_fix_suggestion,
    diagnose_project,
    get_diagnosis_summary
)


def test_dependency_declared():
    assert check_dependency_declared(
        "requests",
        ["requests"]
    ) is True


def test_dependency_not_declared():
    assert check_dependency_declared(
        "pandas",
        ["requests"]
    ) is False


def test_dependency_declared_with_version():
    assert check_dependency_declared(
        "requests",
        ["requests==2.31.0"]
    ) is True


def test_dependency_not_declared_with_other_package():
    assert check_dependency_declared(
        "requests",
        ["pandas", "fastapi"]
    ) is False


def test_diagnose_missing_declaration():

    with patch(
        "pyfixit.diagnostics.check_dependency_installed",
        return_value=True
    ):

        result = diagnose_dependency(
            "pandas",
            []
        )

    assert result["module"] == "pandas"
    assert result["declared"] is False
    assert result["status"] == "missing_declaration"


def test_diagnose_scikit_learn_mapping():
    result = diagnose_dependency(
        "sklearn",
        ["scikit-learn"]
    )

    assert result["module"] == "sklearn"
    assert result["package_name"] == "scikit-learn"
    assert result["import_name"] == "sklearn"
    assert result["declared"] is True


def test_fix_missing_installation():
    result = {
        "module": "requests",
        "package_name": "requests",
        "status": "missing_installation"
    }

    fix = get_fix_suggestion(result)

    assert fix == "pip install requests"


def test_fix_missing_declaration_and_installation():
    result = {
        "module": "pandas",
        "package_name": "pandas",
        "status": "missing_declaration_and_installation"
    }

    fix = get_fix_suggestion(result)

    assert "pip install pandas" in fix
    assert "requirements.txt" in fix


def test_fix_version_conflict():
    result = {
        "module": "pip",
        "package_name": "pip",
        "status": "version_conflict",
        "operator": "==",
        "required_version": "23.0.0"
    }

    fix = get_fix_suggestion(result)

    assert fix == "pip install pip==23.0.0"



def test_diagnose_project():

    result = diagnose_project(".")

    assert "dependencies" in result
    assert "unused_dependencies" in result


def test_dependency_result_structure():

    result = diagnose_project(".")

    for dependency in result["dependencies"]:

        assert "module" in dependency
        assert "package_name" in dependency
        assert "import_name" in dependency
        assert "declared" in dependency
        assert "installed" in dependency
        assert "installed_version" in dependency
        assert "required_version" in dependency
        assert "operator" in dependency
        assert "status" in dependency


def test_valid_statuses():

    result = diagnose_project(".")

    valid_statuses = {
        "ok",
        "missing_installation",
        "missing_declaration",
        "missing_declaration_and_installation",
        "version_conflict"
    }

    for dependency in result["dependencies"]:

        assert dependency["status"] in valid_statuses




def test_get_diagnosis_summary():
    diagnosis = {
        "dependencies": [
            {"status": "ok"},
            {"status": "missing_installation"},
            {"status": "missing_declaration"}
        ],
        "unused_dependencies": [
            "numpy"
        ]
    }

    summary = get_diagnosis_summary(diagnosis)

    assert summary["total_dependencies"] == 3
    assert summary["problems"] == 2
    assert summary["unused_dependencies"] == 1