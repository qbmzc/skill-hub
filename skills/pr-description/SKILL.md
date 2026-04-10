---
name: pr-description
description: >-
  Writes pull request descriptions with context, test plan, and risk notes from
  branch name, commits, and diff. Use when opening a PR, filling PR templates,
  or summarizing changes for reviewers.
---

# Pull Request Description

## Instructions

1. Summarize **user-visible impact** in one short paragraph.
2. List **technical changes** as bullets (components, migrations, flags).
3. Add **how to test** (steps or commands).
4. Call out **risks**, **rollout** (feature flag, migration order), and
   **follow-ups** if any.

## Template

```markdown
## Summary
…

## Changes
- …

## Test plan
- [ ] …

## Risk / rollout
…

## Screenshots (if UI)
…
```

Keep the description scannable; link tickets and design docs when provided.
