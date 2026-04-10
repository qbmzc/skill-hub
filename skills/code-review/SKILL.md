---
name: code-review
description: >-
  Reviews code for correctness, security, maintainability, and test coverage
  using a concise checklist. Use when reviewing pull requests, diffs, or when
  the user asks for a code review or PR feedback.
---

# Code Review

## Instructions

1. Read the changed files and surrounding context; infer intent from the diff.
2. Classify findings by severity (must fix / should fix / nit).
3. Prefer concrete suggestions: file, behavior, and a minimal fix direction.
4. Do not expand scope beyond the request unless blocking issues appear.

## Checklist

- **Correctness**: Edge cases, null/empty paths, concurrency, idempotency.
- **Security**: Injection, authz, secrets, unsafe deserialization, XSS/CSRF
  where relevant.
- **APIs**: Backward compatibility, error contracts, versioning if public.
- **Performance**: N+1 queries, unbounded loops, large allocations in hot paths.
- **Observability**: Logging at wrong level, missing context on errors.
- **Tests**: Behavior covered; flaky patterns; missing regression for fixed bugs.

## Output format

Use bullets grouped by severity:

- **Blocking**: …
- **Should fix**: …
- **Nits**: …

End with a one-line **Verdict**: approve / approve with nits / request changes.
