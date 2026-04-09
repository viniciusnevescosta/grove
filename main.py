#!/usr/bin/env python3
import importlib
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
    1: ("feat", "✨ feat - A new feature was added"),
    2: ("fix", "🐛 fix - A bug was fixed"),
    3: ("docs", "📚 docs - Documentation was added or updated"),
    4: ("test", "🧪 test - Tests were added or modified"),
    5: ("build", "➕ build - Build system or dependency changes"),
    6: ("perf", "⚡ perf - Performance improvements"),
    7: ("style", "🎨 style - Formatting or style-only changes"),
    8: ("refactor", "♻️ refactor - Code restructuring without behavior changes"),
    9: ("chore", "🔧 chore - Maintenance and routine tasks"),
    10: ("ci", "🧱 ci - CI/CD configuration or script changes"),
    11: ("revert", "⏪ revert - Reverting previous changes"),
    12: ("security", "🔒 security - Security-related changes"),
    13: ("wip", "🚧 wip - Work in progress"),
    14: ("raw", "🗃️ raw - Raw data or dataset updates"),
    15: ("cleanup", "🧹 cleanup - Cleanup or dead code removal"),
    16: ("remove", "🗑️ remove - Files or code were removed"),
    17: ("locale", "🌐 locale - Localization updates"),
    18: ("access", "♿ access - Accessibility improvements"),
    19: ("ux", "💄 ux - User interface or experience changes"),
    20: ("custom", "🧩 Custom - Provide your own Conventional Commit type"),
}

BRANCH_TYPES: Dict[int, Tuple[str, str]] = {
    1: ("feat", "✨ feat - For new features"),
    2: ("fix", "🐛 fix - For bug fixes"),
    3: ("hotfix", "🚑 hotfix - For urgent fixes"),
    4: ("release", "🚀 release - For release preparation"),
    5: ("chore", "🔧 chore - For maintenance tasks"),
    6: ("custom", "🧩 Custom - Provide your own branch type"),
}

CUSTOM_COMMIT_TYPE_KEY = max(COMMIT_TYPES)
CUSTOM_BRANCH_TYPE_KEY = max(BRANCH_TYPES)


def enable_line_editing() -> None:
    if sys.platform.startswith("win"):
        return

    try:
        importlib.import_module("readline")
    except ImportError:
        pass



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



def confirm_action(message: str) -> bool:
    confirm = input(message).strip().lower()
    return confirm in ("", "y", "yes")



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



def normalize_multiline_text(value: str) -> str:
    return value.replace("/br", "\n").strip()



def is_valid_custom_commit_type(value: str) -> bool:
    return bool(re.fullmatch(r"[A-Za-z][A-Za-z0-9-]*", value.strip()))



def is_valid_scope(value: str) -> bool:
    return bool(re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._/-]*", value.strip()))



def is_valid_custom_branch_type(value: str) -> bool:
    return bool(re.fullmatch(r"[A-Za-z][A-Za-z0-9-]*", value.strip()))



def format_commit_message(
    commit_type: str,
    description: str,
    body: str,
    scope: str = "",
    breaking_change: bool = False,
) -> str:
    header = commit_type
    if scope:
        header += f"({scope})"
    if breaking_change:
        header += "!"
    header += f": {description}"

    if body:
        return f"{header}\n\n{body}"
    return header



def slugify_branch_description(description: str) -> str:
    value = description.strip().lower()
    value = re.sub(r"[ _]+", "-", value)
    value = re.sub(r"[^a-z0-9/-]", "-", value)
    value = re.sub(r"-+", "-", value)
    value = value.strip("-/")
    return value



def normalize_branch_type(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9-]", "-", value)
    value = re.sub(r"-+", "-", value)
    return value.strip("-")



def prompt_for_files() -> List[str]:
    while True:
        raw_files = get_valid_input(
            "Enter the files to commit (separate with spaces): ",
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



def find_first_valid_type_index(
    args: List[str],
    valid_types: Dict[int, Tuple[str, str]],
) -> Optional[int]:
    for index, value in enumerate(args):
        if value.isdigit() and int(value) in valid_types:
            return index
    return None



def extract_push_flag(args: List[str]) -> Tuple[List[str], bool]:
    filtered_args: List[str] = []
    push_after_commit = False

    for value in args:
        if value == "-p":
            push_after_commit = True
            continue
        filtered_args.append(value)

    return filtered_args, push_after_commit



def parse_commit_arguments(args: List[str]) -> Tuple[List[str], Optional[int], Optional[str], Optional[str]]:
    type_index = find_first_valid_type_index(args, COMMIT_TYPES)

    if type_index is None:
        return args, None, None, None

    files = args[:type_index]
    metadata = args[type_index:]

    commit_type = int(metadata[0]) if metadata else None
    description = metadata[1] if len(metadata) >= 2 else None
    body = " ".join(metadata[2:]) if len(metadata) >= 3 else None

    return files, commit_type, description, body



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



def files_have_pending_changes(files_to_add: List[str]) -> bool:
    try:
        result = subprocess.run(
            ["git", "status", "--porcelain", "--", *files_to_add],
            check=True,
            text=True,
            capture_output=True,
        )
        return bool(result.stdout.strip())
    except subprocess.CalledProcessError as error:
        print_color("Error while checking file changes.", "red")
        if error.stderr:
            print_color(error.stderr, "red")
        sys.exit(1)



def stage_files(files_to_add: List[str]) -> None:
    try:
        subprocess.run(
            ["git", "add", "--", *files_to_add],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
            text=True,
        )
    except subprocess.CalledProcessError as error:
        print_color(f"Error staging files: {error.stderr}", "red")
        sys.exit(1)



def has_staged_changes_for_files(files_to_add: List[str]) -> bool:
    try:
        subprocess.run(
            ["git", "diff", "--cached", "--quiet", "--", *files_to_add],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        return False
    except subprocess.CalledProcessError as error:
        if error.returncode == 1:
            return True
        raise



def get_current_branch() -> str:
    try:
        result = subprocess.run(
            ["git", "branch", "--show-current"],
            check=True,
            text=True,
            capture_output=True,
        )
        branch = result.stdout.strip()
        if not branch:
            print_color("Error: Could not determine the current branch (detached HEAD?).", "red")
            sys.exit(1)
        return branch
    except subprocess.CalledProcessError as error:
        print_color("Error: Could not determine the current branch.", "red")
        if error.stderr:
            print_color(error.stderr, "red")
        sys.exit(1)



def ensure_origin_remote() -> None:
    try:
        subprocess.run(
            ["git", "remote", "get-url", "origin"],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
            text=True,
        )
    except subprocess.CalledProcessError as error:
        print_color("Error: Remote 'origin' was not found.", "red")
        if error.stderr:
            print_color(error.stderr, "red")
        sys.exit(1)



def has_upstream() -> bool:
    try:
        subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}"],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            text=True,
        )
        return True
    except subprocess.CalledProcessError:
        return False



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



def resolve_commit_type_value(selected_type: int) -> str:
    type_str, _ = COMMIT_TYPES[selected_type]
    if selected_type != CUSTOM_COMMIT_TYPE_KEY:
        return type_str

    return get_valid_input(
        "Enter the custom commit type (example: system): ",
        is_valid_custom_commit_type,
    ).lower()



def resolve_branch_type_value(selected_type: int) -> str:
    type_str, _ = BRANCH_TYPES[selected_type]
    if selected_type != CUSTOM_BRANCH_TYPE_KEY:
        return type_str

    custom_type = get_valid_input(
        "Enter the custom branch type (example: system): ",
        is_valid_custom_branch_type,
    )
    return normalize_branch_type(custom_type)



def resolve_commit_scope() -> str:
    return get_valid_input(
        "Enter the optional scope (press Enter to skip): ",
        lambda x: is_valid_scope(x) or x == "",
        optional=True,
    )



def resolve_breaking_change() -> bool:
    response = input("Is this a breaking change? [y/N] ").strip().lower()
    return response in ("y", "yes")



def resolve_commit_description(description: Optional[str]) -> str:
    if description is not None:
        normalized = description.strip()
        if normalized:
            return normalized
        print_color("Error: Commit description cannot be empty.", "red")
        sys.exit(1)

    return get_valid_input(
        "Enter the commit description: ",
        lambda x: bool(x.strip()),
    )



def resolve_commit_body(body: Optional[str]) -> str:
    if body is not None:
        return normalize_multiline_text(body)

    return normalize_multiline_text(
        get_valid_input(
            "Enter the optional commit body or footer text (use '/br' for new lines, press Enter to skip): ",
            lambda x: True,
            optional=True,
        )
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



def create_commit(
    files_to_add: List[str],
    commit_type: Optional[int],
    description: Optional[str],
    body: Optional[str],
    push_after_commit: bool = False,
) -> None:
    if not files_to_add:
        files_to_add = prompt_for_files()

    if not files_have_pending_changes(files_to_add):
        print_color(
            "Error: The provided files do not have pending changes to commit.",
            "red",
        )
        sys.exit(1)

    selected_commit_type = resolve_commit_type(commit_type)
    type_str = resolve_commit_type_value(selected_commit_type)
    scope = resolve_commit_scope()
    breaking_change = resolve_breaking_change()
    resolved_description = resolve_commit_description(description)
    resolved_body = resolve_commit_body(body)

    full_message = format_commit_message(
        commit_type=type_str,
        description=resolved_description,
        body=resolved_body,
        scope=scope,
        breaking_change=breaking_change,
    )

    print_color("\nFiles to commit:", "blue")
    for file_path in files_to_add:
        print(f"- {file_path}")

    print_color("\nCommit message preview:", "blue")
    print(full_message)

    if push_after_commit:
        print_color("\nPush after commit: enabled", "blue")

    if not confirm_action("\nConfirm commit? [Y/n] "):
        print_color("Operation cancelled.", "yellow")
        sys.exit(0)

    stage_files(files_to_add)

    if not has_staged_changes_for_files(files_to_add):
        print_color(
            "Error: No staged changes were found for the provided files after git add.",
            "red",
        )
        sys.exit(1)

    try:
        result = subprocess.run(
            ["git", "commit", "--only", "-m", full_message, "--", *files_to_add],
            check=True,
            text=True,
            capture_output=True,
        )
        print_color("\n✓ Commit created successfully!", "green")
        print(result.stdout)
        if result.stderr:
            print(result.stderr)
    except subprocess.CalledProcessError as error:
        print_color("\n✗ Error creating commit:", "red")
        if error.stderr:
            print_color(error.stderr, "red")
        else:
            print_color(str(error), "red")
        sys.exit(1)
    except KeyboardInterrupt:
        print_color("\nOperation cancelled by user.", "yellow")
        sys.exit(1)

    if push_after_commit:
        print_color("\nCommit finished. Starting push...", "blue")
        push_current_branch()



def create_branch(branch_type: Optional[int], description: Optional[str]) -> None:
    selected_branch_type = resolve_branch_type(branch_type)
    type_str = resolve_branch_type_value(selected_branch_type)

    resolved_description = resolve_branch_description(description)
    slug = slugify_branch_description(resolved_description)
    branch_name = f"{type_str}/{slug}"

    print_color("\nBranch name preview:", "blue")
    print(branch_name)

    if not confirm_action("\nConfirm branch creation? [Y/n] "):
        print_color("Operation cancelled.", "yellow")
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



def push_current_branch() -> None:
    ensure_origin_remote()
    branch = get_current_branch()

    print_color(f"Pushing current branch to remote: {branch}", "blue")

    command = ["git", "push", "origin", branch]
    if not has_upstream():
        command = ["git", "push", "-u", "origin", branch]

    try:
        result = subprocess.run(
            command,
            check=True,
            text=True,
            capture_output=True,
        )
        print_color(f"\n✓ Branch '{branch}' pushed successfully!", "green")
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print(result.stderr)
    except subprocess.CalledProcessError as error:
        print_color("\n✗ Error pushing branch:", "red")
        if error.stderr:
            print_color(error.stderr, "red")
        else:
            print_color(str(error), "red")
        sys.exit(1)



def pull_current_branch() -> None:
    ensure_origin_remote()
    branch = get_current_branch()

    print_color(f"Pulling remote changes into current branch: {branch}", "blue")

    try:
        result = subprocess.run(
            ["git", "pull", "origin", branch],
            check=True,
            text=True,
            capture_output=True,
        )
        print_color(f"\n✓ Branch '{branch}' pulled successfully!", "green")
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print(result.stderr)
    except subprocess.CalledProcessError as error:
        print_color("\n✗ Error pulling branch:", "red")
        if error.stderr:
            print_color(error.stderr, "red")
        else:
            print_color(str(error), "red")
        sys.exit(1)



def print_usage() -> None:
    print_color("Usage:", "blue")
    print("  grove -c <files...>")
    print("  grove -c -p <files...>")
    print("  grove -cp <files...>")
    print("  grove -c <files...> <type-number> <description> [body]")
    print("  grove -c -p <files...> <type-number> <description> [body]")
    print("  grove -cp <files...> <type-number> <description> [body]")
    print("  grove -b")
    print("  grove -b <type-number> [description]")
    print("  grove push")
    print("  grove pull")
    print("\nExamples:")
    print("  grove -c src/main.py README.md")
    print("  grove -c -p src/main.py README.md")
    print("  grove -cp src/main.py README.md")
    print('  grove -c src/main.py README.md 1 "add login page"')
    print('  grove -cp src/main.py 20 "send API event" "BREAKING CHANGE: endpoint contract changed"')
    print("  grove -b 1 add-login-page")
    print("  grove -b 6 observability-pipeline")
    print("  grove push")
    print("  grove pull")



def main() -> None:
    enable_line_editing()

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
        commit_args, push_after_commit = extract_push_flag(extra_args)
        files_to_add, commit_type, description, body = parse_commit_arguments(commit_args)
        create_commit(files_to_add, commit_type, description, body, push_after_commit)
    elif mode == "-cp":
        files_to_add, commit_type, description, body = parse_commit_arguments(extra_args)
        create_commit(files_to_add, commit_type, description, body, True)
    elif mode == "-b":
        branch_type, description = parse_branch_arguments(extra_args)
        create_branch(branch_type, description)
    elif mode == "push":
        if extra_args:
            print_color("Error: 'grove push' does not accept additional arguments.", "red")
            print_usage()
            sys.exit(1)
        push_current_branch()
    elif mode == "pull":
        if extra_args:
            print_color("Error: 'grove pull' does not accept additional arguments.", "red")
            print_usage()
            sys.exit(1)
        pull_current_branch()
    else:
        print_color(f"Error: Unknown flag or command '{mode}'.", "red")
        print_usage()
        sys.exit(1)


if __name__ == "__main__":
    main()
