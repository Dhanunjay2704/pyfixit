PACKAGE_IMPORT_NAMES = {
    "scikit-learn": "sklearn",
    "beautifulsoup4": "bs4",
    "pillow": "PIL",
    "python-dateutil": "dateutil",
    "opencv-python": "cv2"
}


def get_import_name(package_name):
    package_name = package_name.lower()

    if package_name in PACKAGE_IMPORT_NAMES:
        return PACKAGE_IMPORT_NAMES[package_name]

    return package_name


def get_package_name(import_name):
    import_name = import_name.lower()

    for package_name, mapped_import_name in PACKAGE_IMPORT_NAMES.items():
        if mapped_import_name.lower() == import_name:
            return package_name

    return import_name