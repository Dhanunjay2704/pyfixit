from pyfixit.cleaner import clean_requirements


def test_clean_requirements(tmp_path):

    requirements = tmp_path / "requirements.txt"

    requirements.write_text(
        "requests\n"
        "some-unused-package\n"
        "fastapi\n",
        encoding="utf-8"
    )

    (tmp_path / "app.py").write_text(
        "import requests\n"
        "import fastapi\n",
        encoding="utf-8"
    )

    removed = clean_requirements(
        tmp_path,
        apply=False
    )

    assert removed == ["some-unused-package"]

    content = requirements.read_text(
        encoding="utf-8"
    )

    assert "requests" in content
    assert "fastapi" in content
    assert "some-unused-package" in content


def test_clean_requirements_apply(tmp_path):

    requirements = tmp_path / "requirements.txt"

    requirements.write_text(
        "requests\n"
        "some-unused-package\n"
        "fastapi\n",
        encoding="utf-8"
    )

    (tmp_path / "app.py").write_text(
        "import requests\n"
        "import fastapi\n",
        encoding="utf-8"
    )

    removed = clean_requirements(
        tmp_path,
        apply=True
    )

    assert removed == ["some-unused-package"]

    content = requirements.read_text(
        encoding="utf-8"
    )

    assert "requests" in content
    assert "fastapi" in content
    assert "some-unused-package" not in content


def test_clean_requirements_keeps_versioned_dependencies(tmp_path):

    requirements = tmp_path / "requirements.txt"

    requirements.write_text(
        "requests==2.30.0\n"
        "some-unused-package==1.0.0\n",
        encoding="utf-8"
    )

    (tmp_path / "app.py").write_text(
        "import requests\n",
        encoding="utf-8"
    )

    removed = clean_requirements(
        tmp_path,
        apply=True
    )

    assert removed == ["some-unused-package==1.0.0"]

    content = requirements.read_text(
        encoding="utf-8"
    )

    assert "requests==2.30.0" in content
    assert "some-unused-package==1.0.0" not in content


def test_clean_requirements_multiple_unused(tmp_path):

    requirements = tmp_path / "requirements.txt"

    requirements.write_text(
        "requests\n"
        "unused-one\n"
        "fastapi\n"
        "unused-two\n",
        encoding="utf-8"
    )

    (tmp_path / "app.py").write_text(
        "import requests\n"
        "import fastapi\n",
        encoding="utf-8"
    )

    removed = clean_requirements(
        tmp_path,
        apply=True
    )

    assert removed == [
        "unused-one",
        "unused-two"
    ]


def test_clean_requirements_empty_requirements(tmp_path):

    requirements = tmp_path / "requirements.txt"

    requirements.write_text(
        "",
        encoding="utf-8"
    )

    (tmp_path / "app.py").write_text(
        "import requests\n",
        encoding="utf-8"
    )

    removed = clean_requirements(
        tmp_path,
        apply=True
    )

    assert removed == []

    content = requirements.read_text(
        encoding="utf-8"
    )

    assert content == ""