# Grove

Semantic Git helper for commits, branches, push, and pull.

Grove is based on the ideas behind Conventional Commits and Conventional Branch.

- [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) 
- [Conventional Branch](https://conventional-branch.github.io/) 

## Index

- [Features](#features)
- [Installation](#installation)
  - [Using install.py](#using-installpy)
  - [Manual installation](#manual-installation)
  - [Windows](#windows)
  - [macos](#macos)
  - [Linux](#linux)
- [Usage](#usage)
  - [Commit](#commit)
  - [Branch](#branch)
  - [Push](#push)
  - [Pull](#pull)
- [Behavior](#behavior)
- [Branch types](#branch-types)
- [Commit types](#commit-types)
- [Notes](#notes)

## Features

- Interactive semantic commits
- Interactive semantic branches
- Inline command support
- Partial input completion
- Immediate `git add` when using `grove -c <files...>`
- Pushes the current local branch to the current remote branch
- Pulls the current remote branch into the current local branch
- Automatically switches to the new branch with `git checkout -b`

## Installation

You can install Grove manually or run `Install.py`.

### Using install.py

`Install.py` detects the user's operating system and can install, update or uninstall Grove.

Run:

```bash
python Install.py
```

Or choose the action directly:

```bash
python Install.py install
python Install.py update
python Install.py uninstall
```

The installer downloads the main Grove file from the repository and installs it in a user-level location.

### Manual installation

You can also install Grove manually.

Main file:

```txt
https://github.com/viniciusnevescosta/grove/blob/main/grove.py
```

### Windows

#### With install.py

```bash
python Install.py install
```

#### Manual

1. Install Python 3.
2. Download `grove.py`.
3. Save it locally.
4. Run it with:

```bash
python grove.py
```

Optional: create a `grove.bat` file so you can call it as `grove`.

Example `grove.bat`:

```bat
@echo off
python C:\path\to\grove.py %*
```

### macOS

#### With install.py

```bash
python3 Install.py install
```

#### Manual

1. Make sure Python 3 is installed.
2. Save the script as `grove`.
3. Add this shebang at the top of the file:

```python
#!/usr/bin/env python3
```

4. Make it executable:

```bash
chmod +x grove
```

5. Move it to a directory in your `PATH`, for example:

```bash
mv grove ~/.local/bin/grove
```

### Linux

#### With install.py

```bash
python3 Install.py install
```

#### Manual

1. Make sure Python 3 is installed.
2. Save the script as `grove`.
3. Add this shebang at the top of the file:

```python
#!/usr/bin/env python3
```

4. Make it executable:

```bash
chmod +x grove
```

5. Move it to a directory in your `PATH`, for example:

```bash
mv grove ~/.local/bin/grove
```

## Usage

### Commit

```bash
grove -c <files...>
grove -c <files...> <type-number> <title> [description]
```

Examples:

```bash
grove -c src/main.py README.md
grove -c src/main.py README.md 1 add-login-page
grove -c src/main.py 2 fix-header-bug "fix mobile navigation overlap"
```

When you run `grove -c <files...>`, Grove immediately stages the provided files with `git add` before continuing the commit flow.

### Branch

```bash
grove -b
grove -b <type-number> [description]
```

Examples:

```bash
grove -b
grove -b 1 add-login-page
grove -b 2 fix-header-bug
```

- Use `/br` in commit descriptions to create line breaks

### Push

```bash
grove push
```

Pushes all local changes from the current branch to the current remote branch.

### Pull

```bash
grove pull
```

Pulls all remote changes from the current remote branch into the current local branch.

## Behavior

If you provide only part of the command, Grove completes the remaining steps interactively.

Examples:

- if you provide files only, it stages them and asks for the commit type, title, and description
- if you provide files and type, it asks only for the missing title and description
- if you provide branch type only, it asks only for the description

## Branch types

- `feat`
- `fix`
- `hotfix`
- `release`
- `chore`

Branch format:

```txt
<type>/<description>
```

Example:

```txt
feat/add-login-page
```

## Commit types

Grove supports semantic commit selection through a numeric menu.

Example output:

```txt
[feat] add login page
```

## Notes

- Branch descriptions are normalized to slug format
- Commit descriptions are optional
- `grove push` uses the current branch name
- `grove pull` pulls from the branch with the same name on `origin`
- `Install.py` supports install and uninstall
