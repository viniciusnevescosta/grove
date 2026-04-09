import { meta } from './stillOrbit';

export const docsContent = {
  meta,
  toc: [
    { id: 'features', label: 'Features' },
    {
      id: 'installation',
      label: 'Installation',
      children: [
        { id: 'using-install-py', label: 'Using install.py' },
        { id: 'manual-installation', label: 'Manual installation' },
        { id: 'windows', label: 'Windows' },
        { id: 'macos-linux', label: 'macOS / Linux' },
      ],
    },
    {
      id: 'usage',
      label: 'Usage',
      children: [
        { id: 'commit', label: 'Commit' },
        { id: 'commit-and-push', label: 'Commit and push' },
        { id: 'branch', label: 'Branch' },
        { id: 'push', label: 'Push' },
        { id: 'pull', label: 'Pull' },
      ],
    },
    { id: 'behavior', label: 'Behavior' },
    { id: 'commit-types', label: 'Commit types' },
    { id: 'branch-types', label: 'Branch types' },
  ] as const,
  features: [
    {
      title: 'Interactive commits',
      description:
        'Guides you through semantic commits when arguments are missing and keeps the flow fast when they are present.',
    },
    {
      title: 'Interactive branches',
      description:
        'Creates semantic branch names from a guided prompt and switches to the branch automatically.',
    },
    {
      title: 'Inline command support',
      description:
        'Accepts partial or complete commands directly from the shell without forcing a fully interactive flow every time.',
    },
    {
      title: 'Explicit staging only',
      description:
        'Stages only the files you passed to the command instead of adding unrelated changes from the repository.',
    },
    {
      title: 'Commit and push',
      description:
        'Supports one-step commit and push with `-cp` or `-c -p`, using the current branch as the remote target.',
    },
    {
      title: 'Smart remote behavior',
      description:
        'Pushes and pulls against the matching branch on `origin`, setting upstream automatically when needed.',
    },
    {
      title: 'Safer confirmation flow',
      description:
        'All `git add` and `git commit` actions happen only after the final confirmation prompt.',
    },
    {
      title: 'Branch checkout included',
      description:
        'New branches are created with the expected semantic format and opened immediately with `git checkout -b`.',
    },
  ] as const,
  branchTypes: [
    ['feat', 'For new features.'],
    ['fix', 'For bug fixes.'],
    ['hotfix', 'For urgent fixes.'],
    ['release', 'For release preparation.'],
    ['chore', 'For non-code tasks such as dependency or docs updates.'],
  ] as const,
  commitTypes: [
    ['feat', 'New feature added to the application.'],
    ['fix', 'Bug fix in the codebase.'],
    ['docs', 'Documentation added or updated.'],
    ['test', 'Tests added or modified.'],
    ['build', 'Changes to build process or dependencies.'],
    ['perf', 'Performance optimization.'],
    ['style', 'Formatting or style improvements without logic changes.'],
    ['refactor', 'Code restructuring without changing functionality.'],
    ['chore', 'Routine maintenance and non-functional changes.'],
    ['ci', 'Changes to CI/CD configuration or scripts.'],
    ['revert', 'Reverting previous changes.'],
    ['security', 'Security-related improvements or fixes.'],
    ['wip', 'Temporary work in progress commit.'],
    ['raw', 'Updates to raw datasets or data files.'],
    ['cleanup', 'Code cleanup or dead code removal.'],
    ['remove', 'Files or code were removed.'],
    ['locale', 'Translation or localization updates.'],
    ['access', 'Accessibility improvements.'],
    ['ux', 'User interface or user experience changes.'],
    ['break', 'Backward-incompatible breaking change.'],
  ] as const,
  installPyUsage: `python install.py
python install.py install
python install.py update
python install.py uninstall`,
  windowsBat: `@echo off
python C:\path\to\main.py %*`,
  unixInstall: `#!/usr/bin/env python3

chmod +x grove
mv grove ~/.local/bin/grove`,
  commitUsage: `grove -c <files...>
grove -c <files...> <type-number> <title> [description]`,
  commitExamples: `grove -c src/main.py README.md
grove -c src/main.py README.md 1 add-login-page
grove -c src/main.py 2 fix-header-bug "fix mobile navigation overlap"`,
  commitPushUsage: `grove -cp <files...>
grove -cp <files...> <type-number> <title> [description]

grove -c -p <files...>
grove -c -p <files...> <type-number> <title> [description]`,
  commitPushExamples: `grove -cp src/main.py README.md
grove -cp src/main.py README.md 1 add-login-page
grove -c -p src/main.py 2 fix-header-bug "fix mobile navigation overlap"`,
  branchUsage: `grove -b
grove -b <type-number> [description]`,
  branchExamples: `grove -b
grove -b 1 add-login-page
grove -b 2 fix-header-bug`,
  branchFormat: `<type>/<description>`,
  branchExample: `feat/add-login-page`,
  commitOutput: `[feat] add login page`,
  terminalPreview: `$ grove -c src/main.py README.md
$ grove -cp src/main.py 1 add-login-page
$ grove -b 2 fix-header-bug
$ grove push`,
} as const;
