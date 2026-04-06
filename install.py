import platform
import site
import stat
import sys
import urllib.request
from pathlib import Path


SOURCE_BLOB_URLS = [
    "https://github.com/viniciusnevescosta/grove/blob/main/main.py",
    "https://github.com/viniciusnevescosta/grove/blob/release/main/main.py",
]


def print_info(message: str) -> None:
    print(f"[grove] {message}")


def blob_to_raw_github_url(url: str) -> str:
    if "github.com" in url and "/blob/" in url:
        return url.replace("https://github.com/", "https://raw.githubusercontent.com/").replace("/blob/", "/")
    return url


def get_system() -> str:
    system = platform.system().lower()
    if system.startswith("win"):
        return "windows"
    if system == "darwin":
        return "macos"
    return "linux"


def download_grove_source() -> str:
    errors: list[str] = []

    for blob_url in SOURCE_BLOB_URLS:
        raw_url = blob_to_raw_github_url(blob_url)
        print_info(f"Trying download from: {raw_url}")

        try:
            with urllib.request.urlopen(raw_url, timeout=15) as response:
                content = response.read().decode("utf-8")

            if not content.strip():
                raise RuntimeError("Downloaded file is empty.")

            return content
        except Exception as error:
            errors.append(f"{raw_url} -> {error}")

    joined_errors = "\n".join(errors)
    raise RuntimeError(f"Could not download grove.py from any configured source:\n{joined_errors}")


def ensure_shebang(content: str) -> str:
    shebang = "#!/usr/bin/env python3\n"
    if content.startswith("#!"):
        return content
    return shebang + content


def get_windows_install_dir() -> Path:
    user_base = site.getuserbase()
    scripts_dir = Path(user_base) / "Scripts"
    scripts_dir.mkdir(parents=True, exist_ok=True)
    return scripts_dir


def get_unix_install_dir() -> Path:
    install_dir = Path.home() / ".local" / "bin"
    install_dir.mkdir(parents=True, exist_ok=True)
    return install_dir


def install_on_windows() -> None:
    install_dir = get_windows_install_dir()
    target_py = install_dir / "grove.py"
    target_cmd = install_dir / "grove.cmd"

    content = download_grove_source()
    target_py.write_text(content, encoding="utf-8")

    wrapper = (
        "@echo off\n"
        "setlocal\n"
        'py -3 "%~dp0grove.py" %*\n'
    )
    target_cmd.write_text(wrapper, encoding="utf-8")

    print_info(f"Installed grove.py to: {target_py}")
    print_info(f"Installed command wrapper to: {target_cmd}")
    print_info(f"Make sure this directory is in your PATH: {install_dir}")


def install_on_unix(system_name: str) -> None:
    install_dir = get_unix_install_dir()
    target = install_dir / "grove"

    content = download_grove_source()
    content = ensure_shebang(content)
    target.write_text(content, encoding="utf-8")

    current_mode = target.stat().st_mode
    target.chmod(current_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)

    print_info(f"Installed grove to: {target}")
    print_info(f"Make sure this directory is in your PATH: {install_dir}")

    shell_hint = 'export PATH="$HOME/.local/bin:$PATH"'
    if system_name == "macos":
        print_info(f"If needed, add this to your shell config (~/.zshrc or ~/.bashrc): {shell_hint}")
    else:
        print_info(f"If needed, add this to your shell config (~/.bashrc, ~/.zshrc, etc.): {shell_hint}")


def uninstall_on_windows() -> None:
    install_dir = get_windows_install_dir()
    target_py = install_dir / "grove.py"
    target_cmd = install_dir / "grove.cmd"

    removed_any = False

    for path in (target_py, target_cmd):
        if path.exists():
            path.unlink()
            print_info(f"Removed: {path}")
            removed_any = True

    if not removed_any:
        print_info("Nothing to uninstall.")


def uninstall_on_unix() -> None:
    install_dir = get_unix_install_dir()
    target = install_dir / "grove"

    if target.exists():
        target.unlink()
        print_info(f"Removed: {target}")
    else:
        print_info("Nothing to uninstall.")


def install_or_update(system_name: str, action: str) -> None:
    if action == "update":
        print_info("Updating Grove...")
    else:
        print_info("Installing Grove...")

    if system_name == "windows":
        install_on_windows()
    else:
        install_on_unix(system_name)


def uninstall(system_name: str) -> None:
    if system_name == "windows":
        uninstall_on_windows()
    else:
        uninstall_on_unix()


def ask_action() -> str:
    while True:
        answer = input(
            "Choose an action: [1] install  [2] update  [3] uninstall\n> "
        ).strip().lower()

        if answer in {"1", "install", "i"}:
            return "install"
        if answer in {"2", "update", "upgrade"}:
            return "update"
        if answer in {"3", "uninstall", "u", "remove"}:
            return "uninstall"

        print_info("Invalid option. Please choose install, update, or uninstall.")


def get_action_from_argv() -> str:
    if len(sys.argv) >= 2:
        action = sys.argv[1].strip().lower()
        if action in {"install", "i"}:
            return "install"
        if action in {"update", "upgrade"}:
            return "update"
        if action in {"uninstall", "u", "remove"}:
            return "uninstall"

        print_info("Unknown action. Use: install, update, or uninstall.")
        sys.exit(1)

    return ask_action()


def main() -> None:
    action = get_action_from_argv()
    system_name = get_system()

    print_info(f"Detected system: {system_name}")
    print_info(f"Selected action: {action}")

    try:
        if action in {"install", "update"}:
            install_or_update(system_name, action)
            print_info("Done.")
            return

        if action == "uninstall":
            uninstall(system_name)
            print_info("Done.")
            return

        print_info("Unsupported action.")
        sys.exit(1)
    except KeyboardInterrupt:
        print_info("Operation cancelled by user.")
        sys.exit(1)
    except Exception as error:
        print_info(f"Error: {error}")
        sys.exit(1)


if __name__ == "__main__":
    main()
