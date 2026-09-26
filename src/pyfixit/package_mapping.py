PACKAGE_IMPORT_MAP = {
    "scikit-learn": "sklearn",
    "beautifulsoup4": "bs4",
    "python-dotenv": "dotenv",
    "pillow": "PIL",
    "opencv-python": "cv2",
    "pyyaml": "yaml"
}


def get_import_name(package_name):
    package_name = package_name.lower()

    if package_name in PACKAGE_IMPORT_MAP:
        return PACKAGE_IMPORT_MAP[package_name]

    return package_name