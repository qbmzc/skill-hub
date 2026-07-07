---
name: review-loop
description: Requirements-driven code review loop for AI-assisted engineering changes. Use when reviewing AI-generated code, validating a feature against a PRD/Jira/acceptance criteria, checking for missed interfaces/fields/exports/negative scenarios, or reducing regression risk before commit, release, or test handoff.
---

# Review Loop

## Core Rule

Review against the requirement, not only against the diff. Treat the diff as a hypothesis that must be proven against user-visible scenarios, API contracts, data flow, exports, async jobs, and reverse operations.

Do not stop at "looks reasonable". Produce a concrete acceptance matrix, a negative checklist, verification commands or cases, and residual risks.

## Workflow

1. Restate the requirement in testable terms.
   - Identify the feature switch, target users, affected pages, affected APIs, fields, exports, async jobs, and permission branches.
   - Separate "must change" from "must not change".

2. Build an acceptance matrix before judging the code.
   Use this shape:

   | Scenario | Page/API | Method | Field/Data | Expected On | Expected Off | Evidence | Status |
   |---|---|---|---|---|---|---|---|

   Fill `Evidence` with file paths, methods, DTO fields, SQL/mapper names, export templates, curl cases, or observed responses. Mark `Status` as `pass`, `fail`, `unknown`, or `not applicable`.

3. Build a negative checklist.
   Include scenarios where the new behavior must not apply:
   - Candidate/assignment lists before a business identity is known
   - Audit trail or immutable historical traces
   - Emails, notifications, or external regulatory artifacts
   - Calculation/statistics endpoints where real identity is part of grouping or aggregation
   - Save/rollback/reassign actions where the backend needs real IDs or names
   - Existing generated files or cached async outputs
   - Permission branches that return different filter lists or DTO shapes

4. Trace data flow end to end.
   For each matrix row, follow:
   `controller -> business/service -> mapper/query -> DTO -> response/export/task/log`.

   Check both directions:
   - Response path: what the user sees or downloads
   - Request path: what the frontend sends back to save, rollback, reassign, filter, or export

5. Review the diff by risk category.
   Call out issues in this order:
   - Incorrect business behavior or missed acceptance criteria
   - Over-application to negative scenarios
   - Data identity corruption, such as replacing IDs/names before persistence or workflow actions
   - Query/filter/count inconsistency
   - Export, async, cache, or historical-file gaps
   - Compatibility with existing field semantics
   - Performance or repeated DB/config reads
   - Dead code, duplicated logic, naming, and maintainability

6. Require proof for ambiguous decisions.
   If the code assumes a field meaning, confirm from existing code or data flow. Common examples:
   - Raw stage vs already-normalized stage
   - Display name vs account ID vs user ID
   - Filter option value vs visible label
   - Current file generation vs previously generated file reuse
   - Sync response vs async export snapshot

7. Produce executable verification.
   Prefer concrete commands or cases:
   - curl/API examples for switch on/off
   - export regeneration steps
   - database preconditions
   - expected key response fragments
   - unit or integration test names to add or run

## Output Format

Start with findings. Do not bury defects under summaries.

Use this structure:

1. Findings
   - Severity, file/line or API, problem, impact, and specific fix.

2. Acceptance Matrix
   - Include every known requirement row.
   - Mark unknowns explicitly instead of assuming coverage.

3. Negative Checklist
   - State which non-target scenarios were checked and which remain unverified.

4. Verification Plan
   - Include switch on/off cases, exports, async/cached files, and reverse operations.

5. Residual Risk
   - Keep this short and concrete.

## Review Standards

- Prefer primary evidence from repository code, SQL, DTOs, mapper XML, route definitions, tests, and actual command output.
- When evidence is missing, say `unknown` and identify the next command or data needed.
- Do not accept "all reader fields" or "all list interfaces" as sufficient scope. Expand them into exact endpoints and fields.
- Do not assume a helper is safe to reuse across business contexts. Verify its inputs have the same semantics.
- Do not classify a regression as historical without proving the same behavior exists on the baseline branch before the AI change.
- If multiple models or agents are used, split roles: requirements coverage, negative scenarios, exports/async/cache, reverse workflows, and code quality.
