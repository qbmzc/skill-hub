---
name: debug-playbook
description: >-
  Structures systematic debugging: reproduce, isolate, form hypotheses, verify,
  and document. Use when investigating bugs, flaky tests, or non-deterministic
  failures.
---

# Debugging Playbook

## Instructions

1. **Reproduce**: Minimal steps, environment, version, seed if applicable.
2. **Isolate**: Binary search (commits, config, inputs); shrink failing case.
3. **Hypothesize**: One theory at a time; state what would falsify it.
4. **Instrument**: Logging or breakpoints at boundaries (I/O, auth, parsing).
5. **Verify fix**: Same repro fails before, passes after; add regression test
   when appropriate.
6. **Document**: Root cause in PR or ticket in one paragraph.

## Output format for the user

- **Symptom**: …
- **Repro**: …
- **Likely cause**: … (confidence: low/medium/high)
- **Next check**: …

Avoid guessing without evidence; prefer one experiment over many theories.
