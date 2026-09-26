from pyfixit.package_names import get_import_name, get_package_name


def test_scikit_learn_import_name():
    assert get_import_name("scikit-learn") == "sklearn"


def test_beautifulsoup_import_name():
    assert get_import_name("beautifulsoup4") == "bs4"


def test_pillow_import_name():
    assert get_import_name("pillow") == "PIL"


def test_dateutil_import_name():
    assert get_import_name("python-dateutil") == "dateutil"


def test_opencv_import_name():
    assert get_import_name("opencv-python") == "cv2"


def test_requests_import_name():
    assert get_import_name("requests") == "requests"


def test_scikit_learn_package_name():
    assert get_package_name("sklearn") == "scikit-learn"


def test_beautifulsoup_package_name():
    assert get_package_name("bs4") == "beautifulsoup4"


def test_pillow_package_name():
    assert get_package_name("PIL") == "pillow"


def test_dateutil_package_name():
    assert get_package_name("dateutil") == "python-dateutil"


def test_opencv_package_name():
    assert get_package_name("cv2") == "opencv-python"


def test_requests_package_name():
    assert get_package_name("requests") == "requests"