import argparse
import json
from pyfixit.diagnostics import diagnose_project, get_fix_suggestion
from pyfixit.cleaner import clean_requirements


def main():

    parser = argparse.ArgumentParser(
        description="Diagnose common Python import and dependency problems."
    )

    parser.add_argument(
    "command",
    nargs="?",
    default="diagnose",
    help="Command to run"
    )

    parser.add_argument(
        "project_directory",
        nargs="?",
        default=".",
        help="Python project directory"
    )

    parser.add_argument(
        "--apply",
        action="store_true",
        help="Apply cleanup changes"
    )

    parser.add_argument(
        "--json",
        action="store_true",
        help="Output diagnosis as JSON"
    )

    parser.add_argument(
        "--version",
        action="version",
        version="PyFixIt 0.1.0"
    )

    args = parser.parse_args()

    # ------------------------------------------------
    # Support: pyfixit .
    # ------------------------------------------------

    if args.command not in ["diagnose", "clean", "check"]:
        args.project_directory = args.command
        args.command = "diagnose"

    # ------------------------------------------------
    # CLEAN
    # ------------------------------------------------

    if args.command == "clean":

        print("PyFixIt v0.1.0")
        print("Python Project Troubleshooter")
        print()

        removed = clean_requirements(
            args.project_directory,
            apply=args.apply
        )

        print("Cleaning requirements.txt")
        print("------------------------------")

        if len(removed) == 0:
            print("Nothing to remove.")

        elif args.apply:

            for dependency in removed:
                print(f"[REMOVED] {dependency}")

            print()
            print(f"{len(removed)} dependencies removed.")

        else:

            for dependency in removed:
                print(f"[REMOVE] {dependency}")

            print()
            print(
                f"{len(removed)} unused dependencies found."
            )

            print(
                "Run 'pyfixit clean --apply' to remove them."
            )

        return
    


    # ------------------------------------------------
    # CHECK
    # ------------------------------------------------

    if args.command == "check":

        print("PyFixIt v0.1.0")
        print("Python Project Troubleshooter")
        print()

        result = diagnose_project(
            args.project_directory
        )

        dependency_problems = 0

        for item in result["dependencies"]:

            if item["status"] != "ok":
                dependency_problems += 1

        unused_count = len(
            result["unused_dependencies"]
        )

        print("Checking project...")
        print()

        if dependency_problems == 0:
            print("[OK] No dependency problems found")
        else:
            print(
                f"[FAIL] {dependency_problems} "
                f"dependency problems found"
            )

        if unused_count == 0:
            print("[OK] No unused dependencies found")
        else:
            print(
                f"[FAIL] {unused_count} "
                f"unused dependencies found"
            )

        print()

        if dependency_problems > 0 or unused_count > 0:
            raise SystemExit(1)

        raise SystemExit(0)
    
    

    # ------------------------------------------------
    # DIAGNOSE
    # ------------------------------------------------

    result = diagnose_project(
        args.project_directory
    )

    if args.json:
        print(json.dumps(result, indent=2))
        
        has_problems = any(
            item["status"] != "ok"
            for item in result["dependencies"]
        )

        if len(result["unused_dependencies"]) > 0:
            has_problems = True

        if has_problems:
            raise SystemExit(1)

        raise SystemExit(0)
    
    print("PyFixIt v0.1.0")
    print("Python Project Troubleshooter")
    print()

    print("Dependencies")
    print("------------------------------")

    has_problems = False

    for item in result["dependencies"]:

        status = item["status"]

        if status == "ok":
            print(f"[OK] {item['module']}")
            continue

        has_problems = True

        if status == "version_conflict":

            print(
                f"[VERSION CONFLICT] {item['module']}"
            )

            print(
                f"  Required: "
                f"{item['operator']}{item['required_version']}"
            )

            print(
                f"  Installed: "
                f"{item['installed_version']}"
            )

            print(
                f"  Fix: "
                f"{get_fix_suggestion(item)}"
            )

            print()

            continue

        print(f"[PROBLEM] {item['module']}")
        print(f"  Status: {status}")
        print(
            f"  Fix: "
            f"{get_fix_suggestion(item)}"
        )

        print()

    print("Unused dependencies")
    print("------------------------------")

    unused = result["unused_dependencies"]

    if len(unused) == 0:

        print("None")

    else:

        has_problems = True

        for dependency in unused:

            print(f"[UNUSED] {dependency}")

            print(
                f"  Fix: Remove "
                f"'{dependency}' from requirements.txt"
            )

    # ------------------------------------------------
    # EXIT CODE
    # ------------------------------------------------

    if has_problems:
        raise SystemExit(1)

    raise SystemExit(0)


if __name__ == "__main__":
    main()