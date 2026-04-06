import re
import subprocess
import sys
from typing import Dict, Tuple

COLORS = {
    "red": "\033[91m",
    "green": "\033[92m",
    "yellow": "\033[93m",
    "blue": "\033[94m",
    "reset": "\033[0m",
}

COMMIT_TYPES: Dict[int, Tuple[str, str]] = {
    1: ("feat", "✨ New feature - A new feature was added to the application"),
    2: ("fix", "🐛 Bug fix - A bug was fixed in the codebase"),
    3: ("docs", "📚 Documentation - Documentation was added or updated"),
    4: ("test", "🧪 Tests - Tests were added or modified"),
    5: ("build", "➕ Build system - Changes to build process or dependencies"),
    6: ("perf", "⚡ Performance - Performance optimization was implemented"),
    7: ("style", "🎨 Code style - Code formatting or style improvements (no logic changes)"),
    8: ("refactor", "♻️ Refactoring - Code restructuring without changing functionality"),
    9: ("chore", "🔧 Chores - Routine tasks/maintenance (non-functional changes)"),
    10: ("ci", "🧱 CI/CD - Changes to CI/CD configuration or scripts"),
    11: ("revert", "⏪ Revert - Reverting previous changes"),
    12: ("security", "🔒 Security - Security-related improvements or fixes"),
    13: ("wip", "🚧 WIP - Work in progress (temporary commit)"),
    14: ("raw", "🗃️ Raw data - Updates to raw datasets or data files"),
    15: ("cleanup", "🧹 Cleanup - Code cleanup or dead code removal"),
    16: ("remove", "🗑️ Removal - Files or code were removed"),
    17: ("locale", "🌐 Localization - Translation or localization updates"),
    18: ("access", "♿ Accessibility - Accessibility improvements"),
    19: ("ux", "💄 UI/UX - User interface/user experience changes"),
    20: ("break", "💥 Breaking change - Changes that break backward compatibility"),
}

BRANCH_TYPES: Dict[int, Tuple[str, str]] = {
    1: ("feat", "✨ Feature - For new features"),
    2: ("fix", "🐛 Fix - For bug fixes"),
    3: ("hotfix", "🚑 Hotfix - For urgent fixes"),
    4: ("release", "🚀 Release - For release preparation"),
    5: ("chore", "🔧 Chore - For non-code tasks like dependency/docs updates"),
}


def print_color(text: str, color: str = "reset") -> None:
    print(f"{COLORS.get(color, '')}{text}{COLORS['reset']}")


def get_valid_input(prompt: str, validation_func, optional: bool = False) -> str:
    while True:
        try:
            value = input(prompt).strip()
            if optional and not value:
                return ""
            if validation_func(value):
                return value
            print_color("Invalid input, please try again.", "yellow")
        except KeyboardInterrupt:
            print_color("\nOperation cancelled by user.", "yellow")
            sys.exit(1)


def is_git_repository() -> bool:
    try:
        subprocess.run(
            ["git", "rev-parse", "--is-inside-work-tree"],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        return True
    except subprocess.CalledProcessError:
        return False


def has_staged_changes() -> bool:
    try:
        subprocess.run(
            ["git", "diff", "--cached", "--quiet"],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        return False
    except subprocess.CalledProcessError as e:
        if e.returncode == 1:
            return True
        raise


def format_commit_message(type_str: str, emoji: str, title: str, description: str) -> str:
    commit_message = f"[{type_str}] {emoji} {title}"
    if description:
        formatted_description = description.replace("/br", "\n")
        commit_message += f"\n\n{formatted_description}"
    return commit_message


def slugify_branch_description(description: str) -> str:
    value = description.strip().lower()
    value = re.sub(r"[ _]+", "-", value)
    value = re.sub(r"[^a-z0-9/-]", "-", value)
    value = re.sub(r"-+", "-", value)
    value = value.strip("-/")
    return value


def create_commit(files_to_add):
    try:
        print_color(f"Staging files: {', '.join(files_to_add)}", "blue")
        subprocess.run(
            ["git", "add", *files_to_add],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
            text=True,
        )
    except subprocess.CalledProcessError as e:
        print_color(f"Error staging files: {e.stderr}", "red")
        sys.exit(1)

    if not has_staged_changes():
        print_color(
            "Error: No changes staged after adding files. Check if files have modifications.",
            "red",
        )
        sys.exit(1)

    print("\nSelect the commit type:")
    for num, (_, desc) in COMMIT_TYPES.items():
        print(f"{num}. {desc}")

    commit_type = int(
        get_valid_input(
            "\nEnter the number corresponding to the commit type: ",
            lambda x: x.isdigit() and int(x) in COMMIT_TYPES,
        )
    )

    type_str, emoji_desc = COMMIT_TYPES[commit_type]
    emoji = emoji_desc.split()[0]

    title = get_valid_input(
        "Enter the commit title (required, max 72 chars): ",
        lambda x: 0 < len(x) <= 72,
    )

    description = get_valid_input(
        "Enter the commit description (optional, use '/br' for new lines, press 'Enter' to skip): ",
        lambda x: True,
        optional=True,
    )

    full_message = format_commit_message(type_str, emoji, title, description)

    print_color("\nCommit message preview:", "blue")
    print(full_message)

    confirm = input("\nConfirm commit? [Y/n] ").strip().lower()
    if confirm not in ("", "y", "yes"):
        print_color("Commit cancelled.", "yellow")
        sys.exit(0)

    try:
        result = subprocess.run(
            ["git", "commit", "-m", full_message],
            check=True,
            text=True,
            capture_output=True,
        )
        print_color("\n✓ Commit created successfully!", "green")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print_color("\n✗ Error creating commit:", "red")
        print_color(e.stderr, "red")
        sys.exit(1)
    except KeyboardInterrupt:
        print_color("\nOperation cancelled by user.", "yellow")
        sys.exit(1)


def create_branch():
    print("\nSelect the branch type:")
    for num, (_, desc) in BRANCH_TYPES.items():
        print(f"{num}. {desc}")

    branch_type = int(
        get_valid_input(
            "\nEnter the number corresponding to the branch type: ",
            lambda x: x.isdigit() and int(x) in BRANCH_TYPES,
        )
    )

    type_str, _ = BRANCH_TYPES[branch_type]

    description = get_valid_input(
        "Enter the branch description (required): ",
        lambda x: len(slugify_branch_description(x)) > 0,
    )

    slug = slugify_branch_description(description)
    branch_name = f"{type_str}/{slug}"

    print_color("\nBranch name preview:", "blue")
    print(branch_name)

    confirm = input("\nConfirm branch creation? [Y/n] ").strip().lower()
    if confirm not in ("", "y", "yes"):
        print_color("Branch creation cancelled.", "yellow")
        sys.exit(0)

    try:
        result = subprocess.run(
            ["git", "checkout", "-b", branch_name],
            check=True,
            text=True,
            capture_output=True,
        )
        print_color(f"\n✓ Branch '{branch_name}' created successfully!", "green")
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print(result.stderr)
    except subprocess.CalledProcessError as e:
        print_color("\n✗ Error creating branch:", "red")
        if e.stderr:
            print_color(e.stderr, "red")
        else:
            print_color(str(e), "red")
        sys.exit(1)
    except KeyboardInterrupt:
        print_color("\nOperation cancelled by user.", "yellow")
        sys.exit(1)


def print_usage():
    print_color("Usage:", "blue")
    print("  grove -c <file1> <file2> ...")
    print("  grove -b")


def main():
    if not is_git_repository():
        print_color("Error: Not a git repository.", "red")
        sys.exit(1)

    if len(sys.argv) < 2:
        print_color("Error: Missing mode flag.", "red")
        print_usage()
        sys.exit(1)

    mode = sys.argv[1]

    if mode == "-c":
        if len(sys.argv) < 3:
            print_color("Error: No files specified for commit mode.", "red")
            print_usage()
            sys.exit(1)
        files_to_add = sys.argv[2:]
        create_commit(files_to_add)
    elif mode == "-b":
        if len(sys.argv) != 2:
            print_color("Error: Branch mode does not accept additional arguments.", "red")
            print_usage()
            sys.exit(1)
        create_branch()
    else:
        print_color(f"Error: Unknown flag '{mode}'.", "red")
        print_usage()
        sys.exit(1)


if __name__ == "__main__":
    main()