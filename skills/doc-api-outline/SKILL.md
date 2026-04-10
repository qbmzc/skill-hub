---
name: doc-api-outline
description: >-
  Produces API documentation outlines: resources, methods, request/response
  shapes, errors, and examples. Use when drafting OpenAPI, README API sections,
  or internal integration docs.
---

# API Documentation Outline

## Instructions

1. Identify **audience** (internal service vs public SDK).
2. For each endpoint: method, path, auth, idempotency, pagination.
3. Document **request** and **response** schemas with required fields and
   formats (date-time, enums).
4. List **errors** with HTTP status, machine-readable code, and recovery hints.
5. Provide **one happy-path example** and one **common failure** example.

## Skeleton

```markdown
## <Resource name>

### <METHOD> <path>
- **Auth**: …
- **Query/body**: …
- **Response 200**: …
- **Errors**: 400 …, 401 …, 404 …, 409 …, 429 …
- **Example**: …
```

Prefer tables for field lists when there are many parameters.
