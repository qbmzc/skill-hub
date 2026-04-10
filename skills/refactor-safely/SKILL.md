---
name: refactor-safely
description: >-
  Plans and executes refactors with minimal behavior change: characterization
  tests, incremental steps, and rollback points. Use when renaming modules,
  extracting functions, or restructuring without a feature change.
---

# Safe Refactoring

## Instructions

1. **Establish a baseline**: Run existing tests; note failing areas before
   starting.
2. **Prefer mechanical steps**: One rename or one extraction per commit when
   possible.
3. **Preserve behavior first**: Defer performance or style cleanups unless
   isolated.
4. **Add tests only when needed** to lock behavior that is currently untested
   and touched by the refactor.
5. After each logical step, run the narrowest test set that covers the change.

## Red flags (stop and re-plan)

- Mixed refactor with feature work in the same commit.
- No tests and high coupling; consider adding thin characterization tests first.
- Public API or schema change without version or migration strategy.

## Suggested commit sequence

1. `refactor: extract X (no behavior change)`
2. `refactor: rename Y for clarity`
3. `test: cover edge case for Z` (if required)
