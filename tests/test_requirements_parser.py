from pyfixit.requirements_parser import parse_requirement, check_version


def test_parse_simple_requirement():
    result = parse_requirement("requests")

    assert result["package"] == "requests"
    assert result["operator"] is None
    assert result["version"] is None


def test_parse_exact_version():
    result = parse_requirement("requests==2.31.0")

    assert result["package"] == "requests"
    assert result["operator"] == "=="
    assert result["version"] == "2.31.0"


def test_parse_minimum_version():
    result = parse_requirement("pandas>=2.0")

    assert result["package"] == "pandas"
    assert result["operator"] == ">="
    assert result["version"] == "2.0"


def test_parse_maximum_version():
    result = parse_requirement("numpy<=2.0")

    assert result["package"] == "numpy"
    assert result["operator"] == "<="
    assert result["version"] == "2.0"


def test_check_exact_version():
    assert check_version(
        "2.31.0",
        "==",
        "2.31.0"
    ) is True


def test_check_wrong_exact_version():
    assert check_version(
        "2.32.0",
        "==",
        "2.31.0"
    ) is False


def test_check_minimum_version():
    assert check_version(
        "2.32.0",
        ">=",
        "2.31.0"
    ) is True


def test_check_less_than_version():
    assert check_version(
        "0.9.0",
        "<",
        "1.0.0"
    ) is True


def test_no_version_requirement():
    assert check_version(
        "2.32.0",
        None,
        None
    ) is True