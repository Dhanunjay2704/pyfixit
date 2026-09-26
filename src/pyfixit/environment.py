import sys


def get_python_version():
    return f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"


def get_python_executable():
    return sys.executable


def is_virtual_environment():
    return sys.prefix != sys.base_prefix


def get_environment_info():
    return {
        "python_version": get_python_version(),
        "python_executable": get_python_executable(),
        "virtual_environment": is_virtual_environment()
    }