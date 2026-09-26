import subprocess
import sys
from pathlib import Path
import json


PROJECT_ROOT = Path(__file__).parent.parent


def run_pyfixit(*args):
    command = [
        sys.executable,
        "-m",
        "pyfixit.cli",
        *args
    ]

    return subprocess.run(
        command,
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True
    )


def test_help():
    result = run_pyfixit("--help")

    assert result.returncode == 0
    assert "Diagnose common Python import and dependency problems." in result.stdout


def test_version():
    result = run_pyfixit("--version")

    assert result.returncode == 0
    assert "PyFixIt 0.1.0" in result.stdout


def test_diagnose_project():
    result = run_pyfixit("diagnose", ".")

    assert result.returncode == 1
    assert "PyFixIt v0.1.0" in result.stdout
    assert "Dependencies" in result.stdout


def test_clean_project():
    result = run_pyfixit("clean", ".")

    assert result.returncode == 0
    assert "Cleaning requirements.txt" in result.stdout


def test_json_output():
    result = run_pyfixit(
        "diagnose",
        ".",
        "--json"
    )

    assert result.returncode == 1
    assert '"dependencies"' in result.stdout
    assert '"unused_dependencies"' in result.stdout
    assert '"status"' in result.stdout


def test_diagnose_json():
    result = run_pyfixit("diagnose", ".", "--json")

    assert result.returncode == 1

    data = json.loads(result.stdout)

    assert "dependencies" in data
    assert "unused_dependencies" in data




def test_check_project_with_problems():
    result = run_pyfixit("check", ".")

    assert result.returncode == 1
    assert "Checking project..." in result.stdout
    assert "[FAIL]" in result.stdout


def test_check_clean_project(tmp_path):
    (tmp_path / "requirements.txt").write_text(
        "requests\n",
        encoding="utf-8"
    )

    (tmp_path / "app.py").write_text(
        "import requests\n",
        encoding="utf-8"
    )

    result = run_pyfixit("check", str(tmp_path))

    assert result.returncode == 0
    assert "Checking project..." in result.stdout
    assert "[OK] No dependency problems found" in result.stdout
    assert "[OK] No unused dependencies found" in result.stdout