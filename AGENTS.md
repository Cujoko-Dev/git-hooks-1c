# Codex Agent Notes

This repository already keeps most project-specific agent guidance in Cursor files.
Codex should use those files as the source of truth instead of duplicating them here.

## Before Making Changes

- Read the relevant files under `.cursor/rules/*.mdc`.
- For architecture or larger changes, read the relevant `.cursor/skills/*/SKILL.md`.
- Treat Cursor rules as project instructions unless they conflict with an explicit user request or higher-priority Codex/system instructions.
- If the local `.notes/` directory exists, check relevant notes there before non-trivial changes, business-logic changes, refactoring, or architecture work.

## Project Notes

Project notes are available in the local `.notes/` directory when it exists.
The `.notes/` directory is local workspace context and may be absent on other machines.

## Common Cursor Rules To Check

- `.cursor/rules/testing-workflow.mdc` and `.cursor/rules/pdm-package-manager.mdc` before Python/test workflow changes.
- `.cursor/rules/auto-commit-message.mdc` before preparing commits.

## Common Cursor Skills To Check

- `.cursor/skills/pdm-dev-workflow/SKILL.md` for PDM-based development workflow.
