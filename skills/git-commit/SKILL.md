---
name: git-commit
description: >-
  Produces clear commit messages from staged or provided diffs, following
  Conventional Commits when appropriate. Use when the user asks for commit
  messages, changelog-style summaries, or how to split commits.
---

# Git Commit Messages

## Instructions

1. Infer scope from paths and symbols touched (`feat`, `fix`, `docs`, `refactor`,
   `test`, `chore`, `perf`, `ci`, `build`).
2. Subject line: imperative mood, ~72 characters, no trailing period.
3. Body: what and why (not how), wrap at ~72 chars; link issues if known.
4. If the diff mixes concerns, suggest splitting into multiple commits.

## Conventional Commits template

```
<type>(<scope>): <short description>

[optional body]

[optional footer: Fixes #123, BREAKING CHANGE: ...]
```

## Examples

**Single feature**

```
feat(auth): add refresh token rotation

Reduces window for stolen refresh tokens; aligns with OAuth BCP.
```

**Bugfix**

```
fix(api): return 404 for missing tenant header

Previously returned 500; clients could not distinguish misconfig from server error.
```
