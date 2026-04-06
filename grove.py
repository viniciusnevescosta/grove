import re
import shlex
import subprocess
import sys
from typing import Dict, List, Optional, Tuple

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
    except subprocess.CalledProcessError as error:
        if error.returncode == 1:
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


def prompt_for_files() -> List[str]:
    while True:
        raw_files = get_valid_input(
            "Enter the files to stage (separate with spaces): ",
            lambda x: bool(x.strip()),
        )
        try:
            files = shlex.split(raw_files)
        except ValueError:
            print_color("Invalid file list. Check your quotes and try again.", "yellow")
            continue

        if files:
            return files

        print_color("Please provide at least one file.", "yellow")


def find_first_valid_type_index(args: List[str], valid_types: Dict[int, Tuple[str, str]]) -> Optional[int]:
    for index, value in enumerate(args):
        if value.isdigit() and int(value) in valid_types:
            return index
    return None


def parse_commit_arguments(args: List[str]) -> Tuple[List[str], Optional[int], Optional[str], Optional[str]]:
    type_index = find_first_valid_type_index(args, COMMIT_TYPES)

    if type_index is None:
        return args, None, None, None

    files = args[:type_index]
    metadata = args[type_index:]

    commit_type = int(metadata[0]) if metadata else None
    title = metadata[1] if len(metadata) >= 2 else None
    description = " ".join(metadata[2:]) if len(metadata) >= 3 else None

    return files, commit_type, title, description


def parse_branch_arguments(args: List[str]) -> Tuple[Optional[int], Optional[str]]:
    if not args:
        return None, None

    branch_type = None
    description = None

    if args[0].isdigit() and int(args[0]) in BRANCH_TYPES:
        branch_type = int(args[0])
        if len(args) >= 2:
            description = " ".join(args[1:])
    else:
        description = " ".join(args)

    return branch_type, description


def stage_files(files_to_add: List[str]) -> None:
    try:
        print_color(f"Staging files: {', '.join(files_to_add)}", "blue")
        subprocess.run(
            ["git", "add", *files_to_add],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
            text=True,
        )
    except subprocess.CalledProcessError as error:
        print_color(f"Error staging files: {error.stderr}", "red")
        sys.exit(1)

    if not has_staged_changes():
        print_color(
            "Error: No changes staged after adding files. Check if files have modifications.",
            "red",
        )
        sys.exit(1)


def resolve_commit_type(commit_type: Optional[int]) -> int:
    if commit_type is not None:
        return commit_type

    print("\nSelect the commit type:")
    for num, (_, desc) in COMMIT_TYPES.items():
        print(f"{num}. {desc}")

    return int(
        get_valid_input(
            "\nEnter the number corresponding to the commit type: ",
            lambda x: x.isdigit() and int(x) in COMMIT_TYPES,
        )
    )


def resolve_branch_type(branch_type: Optional[int]) -> int:
    if branch_type is not None:
        return branch_type

    print("\nSelect the branch type:")
    for num, (_, desc) in BRANCH_TYPES.items():
        print(f"{num}. {desc}")

    return int(
        get_valid_input(
            "\nEnter the number corresponding to the branch type: ",
            lambda x: x.isdigit() and int(x) in BRANCH_TYPES,
        )
    )


def resolve_commit_title(title: Optional[str]) -> str:
    if title is not None:
        if 0 < len(title) <= 72:
            return title
        print_color("Error: Commit title must have between 1 and 72 characters.", "red")
        sys.exit(1)

    return get_valid_input(
        "Enter the commit title (required, max 72 chars): ",
        lambda x: 0 < len(x) <= 72,
    )


def resolve_commit_description(description: Optional[str]) -> str:
    if description is not None:
        return description

    return get_valid_input(
        "Enter the commit description (optional, use '/br' for new lines, press 'Enter' to skip): ",
        lambda x: True,
        optional=True,
    )


def resolve_branch_description(description: Optional[str]) -> str:
    if description is not None:
        slug = slugify_branch_description(description)
        if slug:
            return description
        print_color("Error: Branch description is invalid after normalization.", "red")
        sys.exit(1)

    return get_valid_input(
        "Enter the branch description (required): ",
        lambda x: len(slugify_branch_description(x)) > 0,
    )


def confirm_action(message: str) -> None:
    confirm = input(message).strip().lower()
    if confirm not in ("", "y", "yes"):
        print_color("Operation cancelled.", "yellow")
        sys.exit(0)


def create_commit(files_to_add: List[str], commit_type: Optional[int], title: Optional[str], description: Optional[str]) -> None:
    if not files_to_add:
        files_to_add = prompt_for_files()

    stage_files(files_to_add)

    resolved_commit_type = resolve_commit_type(commit_type)
    type_str, emoji_desc = COMMIT_TYPES[resolved_commit_type]
    emoji = emoji_desc.split()[0]

    resolved_title = resolve_commit_title(title)
    resolved_description = resolve_commit_description(description)

    full_message = format_commit_message(type_str, emoji, resolved_title, resolved_description)

    print_color("\nCommit message preview:", "blue")
    print(full_message)

    confirm_action("\nConfirm commit? [Y/n] ")

    try:
        result = subprocess.run(
            ["git", "commit", "-m", full_message],
            check=True,
            text=True,
            capture_output=True,
        )
        print_color("\n✓ Commit created successfully!", "green")
        print(result.stdout)
    except subprocess.CalledProcessError as error:
        print_color("\n✗ Error creating commit:", "red")
        print_color(error.stderr, "red")
        sys.exit(1)
    except KeyboardInterrupt:
        print_color("\nOperation cancelled by user.", "yellow")
        sys.exit(1)


def create_branch(branch_type: Optional[int], description: Optional[str]) -> None:
    resolved_branch_type = resolve_branch_type(branch_type)
    type_str, _ = BRANCH_TYPES[resolved_branch_type]

    resolved_description = resolve_branch_description(description)
    slug = slugify_branch_description(resolved_description)
    branch_name = f"{type_str}/{slug}"

    print_color("\nBranch name preview:", "blue")
    print(branch_name)

    confirm_action("\nConfirm branch creation? [Y/n] ")

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
    except subprocess.CalledProcessError as error:
        print_color("\n✗ Error creating branch:", "red")
        if error.stderr:
            print_color(error.stderr, "red")
        else:
            print_color(str(error), "red")
        sys.exit(1)
    except KeyboardInterrupt:
        print_color("\nOperation cancelled by user.", "yellow")
        sys.exit(1)


def print_usage() -> None:
    print_color("Usage:", "blue")
    print("  grove -c <files...>")
    print("  grove -c <files...> <type-number> <title> [description]")
    print("  grove -b")
    print("  grove -b <type-number> [description]")
    print("\nExamples:")
    print("  grove -c src/main.py README.md 1 titulo-exemplo descricao-exemplo")
    print('  grove -c src/main.py 1 "titulo exemplo" "descricao exemplo"')
    print("  grove -b 1 add-login-page")


def main() -> None:
    if not is_git_repository():
        print_color("Error: Not a git repository.", "red")
        sys.exit(1)

    if len(sys.argv) < 2:
        print_color("Error: Missing mode flag.", "red")
        print_usage()
        sys.exit(1)

    mode = sys.argv[1]
    extra_args = sys.argv[2:]

    if mode == "-c":
        files_to_add, commit_type, title, description = parse_commit_arguments(extra_args)
        create_commit(files_to_add, commit_type, title, description)
    elif mode == "-b":
        branch_type, description = parse_branch_arguments(extra_args)
        create_branch(branch_type, description)
    else:
        print_color(f"Error: Unknown flag '{mode}'.", "red")
        print_usage()
        sys.exit(1)


if __name__ == "__main__":
    main()