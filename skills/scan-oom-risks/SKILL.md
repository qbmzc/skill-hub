---
name: scan-oom-risks
description: Scan Java/Spring services for OOM, GC pressure, and native-memory risk patterns. Use when reviewing file-processing code, PDF/image/Base64/upload/download paths, JVM/Kubernetes memory settings, heap dump or GC observations, or when asked to find memory leaks, OOM risks, humongous allocations, unclosed streams, or resource-retention problems.
---

# Scan OOM Risks

Use this skill to audit a repository or change set for memory-risk patterns, then turn static matches into prioritized, evidence-backed findings.

## Workflow

1. Determine scope: changed files, a module, or the whole repository. Prefer the narrowest scope that answers the user.
2. Run the scanner when local files are available:

```bash
python3 /path/to/scan-oom-risks/scripts/scan_oom_risks.py <repo-or-module>
```

Use `--json` when another tool or script will consume the results.

3. Read `references/risk-patterns.md` when findings include Java/Spring file upload, PDF, image, Base64, stream handling, JVM, or Kubernetes memory configuration.
4. Validate high-severity matches against real code paths. Do not treat a regex hit as proof of a leak until lifecycle, object size, concurrency, and cleanup behavior are checked.
5. Prioritize by blast radius:
   - P0/P1: request-path large heap allocations, full-file buffering, PDF/image processing of user files, unbounded concurrency, missing cleanup for temp files or native resources.
   - P2: resource leaks on exceptional paths, oversized thresholds, missing observability, risky defaults.
   - P3: hygiene issues, stale comments, low-traffic admin paths.
6. Report findings with file/line evidence, why memory grows, which workload triggers it, and a concrete fix.

## Review Heuristics

- Prefer streaming, bounded buffers, temp files, and random-access file APIs for large user files.
- Treat Base64 strings, `byte[]`, `ByteArrayOutputStream`, `BufferedImage`, PDF readers, multipart upload buffers, and zip generation as high-risk until bounded.
- Check exceptional paths. `close()`, `dispose()`, and temp-file deletion must survive thrown exceptions.
- Separate heap OOM from container OOMKilled. Heap dumps help only JVM-thrown OOM; RSS/native issues need GC logs, NMT, direct-memory metrics, and container memory graphs.
- Be careful with JVM advice. Code-level full buffering usually beats GC tuning. Avoid recommending `G1HeapRegionSize` changes without GC-log evidence.

## Output Shape

Lead with the conclusion, then list findings by severity:

```markdown
Conclusion: ...

Findings
- P1 file:line - Risk title
  Evidence: ...
  Impact: ...
  Recommendation: ...

Verification
- Commands run: ...
- Gaps: ...
```

When no serious issues are found, say so clearly and list residual risks or coverage gaps.
