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
      title: 'Strict Conventional Commit header',
      description:
        'Builds commit messages as `<type>[optional scope][optional !]: <description>` instead of using a custom Grove-specific header.',
    },
    {
      title: 'Interactive scope and breaking flag',
      description:
        'Lets you add an optional scope and mark breaking changes with `!` while keeping the flow guided and fast.',
    },
    {
      title: 'Custom commit and branch types',
      description:
        'The last menu option is `Custom`, so you can create headers like `system(api)!: test` and branches like `system/observability`.',
    },
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
  ] as const,
  branchTypes: [
    ['feat', 'For new features.'],
    ['fix', 'For bug fixes.'],
    ['hotfix', 'For urgent fixes.'],
    ['release', 'For release preparation.'],
    ['chore', 'For maintenance tasks.'],
    ['custom', 'Provide your own branch type, such as `system`.'],
  ] as const,
  commitTypes: [
    ['feat', 'Adds a new feature.'],
    ['fix', 'Represents a bug fix.'],
    ['docs', 'Documentation changes.'],
    ['test', 'Test additions or updates.'],
    ['build', 'Build system or dependency changes.'],
    ['perf', 'Performance improvements.'],
    ['style', 'Formatting or style-only changes.'],
    ['refactor', 'Code restructuring without changing behavior.'],
    ['chore', 'Routine maintenance tasks.'],
    ['ci', 'CI/CD configuration changes.'],
    ['revert', 'Reverts a previous change.'],
    ['security', 'Security-related changes.'],
    ['wip', 'Work in progress.'],
    ['raw', 'Raw data updates.'],
    ['cleanup', 'Cleanup or dead code removal.'],
    ['remove', 'Files or code removals.'],
    ['locale', 'Localization updates.'],
    ['access', 'Accessibility improvements.'],
    ['ux', 'User interface or user experience changes.'],
    ['custom', 'Provide your own type, such as `system`.'],
  ] as const,
  installPyUsage: `python install.py
python install.py install
python install.py update
python install.py uninstall`,
  windowsBat: `@echo off
python C:\\path\\to\\main.py %*`,
  unixInstall: `#!/usr/bin/env python3

chmod +x grove
mv grove ~/.local/bin/grove`,
  commitUsage: `grove -c <files...>
grove -c <files...> <type-number> <description> [body]`,
  commitExamples: `# standard type
feat(parser): add array support

# breaking change
feat(api)!: remove legacy endpoint

# custom type
system(api)!: change auth contract`,
  commitPushUsage: `grove -cp <files...>
grove -cp <files...> <type-number> <description> [body]

grove -c -p <files...>
grove -c -p <files...> <type-number> <description> [body]`,
  commitPushExamples: `grove -cp src/main.py README.md
grove -cp src/main.py README.md 1 "add login page"
grove -c -p src/main.py 20 "change auth contract" "BREAKING CHANGE: token payload changed"`,
  branchUsage: `grove -b
grove -b <type-number> [description]`,
  branchExamples: `grove -b
grove -b 1 add-login-page
grove -b 6 observability-pipeline`,
  branchFormat: `<type>/<description>`,
  branchExample: `system/observability-pipeline`,
  commitOutput: `system(api)!: change auth contract`,
  terminalPreview: `$ grove -c src/main.py README.md
$ grove -cp src/main.py 20 "change auth contract"
$ grove -b 6 observability-pipeline
$ grove push`,
} as const;
