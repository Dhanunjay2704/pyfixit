from packaging.version import Version


def parse_requirement(requirement):
    requirement = requirement.strip()

    if not requirement:
        return None

    operators = ["==", ">=", "<=", "!=", ">", "<"]

    for operator in operators:
        if operator in requirement:
            parts = requirement.split(operator, 1)

            return {
                "package": parts[0].strip(),
                "operator": operator,
                "version": parts[1].strip()
            }

    return {
        "package": requirement,
        "operator": None,
        "version": None
    }





def check_version(installed_version, operator, required_version):
    if installed_version is None:
        return False

    if operator is None or required_version is None:
        return True

    installed = Version(installed_version)
    required = Version(required_version)

    if operator == "==":
        return installed == required

    if operator == ">=":
        return installed >= required

    if operator == "<=":
        return installed <= required

    if operator == ">":
        return installed > required

    if operator == "<":
        return installed < required

    if operator == "!=":
        return installed != required

    return False


