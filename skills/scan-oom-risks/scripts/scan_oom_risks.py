#!/usr/bin/env python3
import argparse
import json
import os
import re
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Iterable, List


EXCLUDED_DIRS = {
    ".git",
    ".idea",
    ".qoder",
    ".gradle",
    ".mvn",
    "target",
    "build",
    "node_modules",
    "dist",
    "out",
    "local-skills",
}

DEFAULT_EXTENSIONS = {
    ".java",
    ".kt",
    ".scala",
    ".properties",
    ".yml",
    ".yaml",
    ".xml",
    ".md",
}


@dataclass
class Rule:
    rule_id: str
    severity: str
    category: str
    pattern: str
    message: str
    recommendation: str


@dataclass
class Finding:
    severity: str
    category: str
    rule_id: str
    path: str
    line: int
    snippet: str
    message: str
    recommendation: str


RULES: List[Rule] = [
    Rule(
        "pdfreader-inputstream",
        "P1",
        "PDF",
        r"new\s+PdfReader\s*\(\s*(is|in|inputStream|.*InputStream|Files\.newInputStream\s*\()",
        "iText PdfReader appears to read from an InputStream, which can fully buffer large PDFs.",
        "Prefer a temp file or file path based PdfReader and close the reader in finally.",
    ),
    Rule(
        "bytearray-output-stream",
        "P1",
        "Heap buffering",
        r"new\s+ByteArrayOutputStream\s*\(",
        "ByteArrayOutputStream may retain a full file or response in heap.",
        "Check max size and prefer streaming directly to the destination.",
    ),
    Rule(
        "to-byte-array",
        "P1",
        "Heap buffering",
        r"\.toByteArray\s*\(",
        "toByteArray creates a full heap copy of buffered data.",
        "Avoid full-copy conversion on user-controlled files; stream or enforce a small limit.",
    ),
    Rule(
        "base64-decode-bytes",
        "P1",
        "Base64",
        r"(decodeBase64|Base64\.get.*Decoder\(\)\.decode|base64DecoderToBytes|getBase64Decode\(.*\)\.decode)",
        "Base64 decoding to byte[] can double memory pressure.",
        "Use decoder-wrapped streams and strict decoded-byte limits.",
    ),
    Rule(
        "base64-encode-bytes",
        "P1",
        "Base64",
        r"(encodeBase64String|base64Encoder\s*\(|Base64\.get.*Encoder\(\)\.encodeToString)",
        "Base64 encoding to String can allocate large intermediate byte[] and char[] objects.",
        "Stream Base64 output or keep the endpoint size limit conservative.",
    ),
    Rule(
        "read-all-bytes",
        "P1",
        "Heap buffering",
        r"(readAllBytes|IOUtils\.toByteArray|FileUtils\.readFileToByteArray|StreamUtils\.copyToByteArray|IOUtils\.toString)",
        "This API may read an entire stream or file into heap.",
        "Use bounded streaming APIs for user-controlled files.",
    ),
    Rule(
        "buffered-image",
        "P1",
        "Image",
        r"(new\s+BufferedImage\s*\(|ImageIO\.read\s*\(|asBufferedImage\s*\()",
        "Image decoding or allocation can create large heap pixel arrays.",
        "Check byte and pixel limits; avoid multiple full-size images at once.",
    ),
    Rule(
        "graphics-create",
        "P2",
        "Native resource",
        r"\.(createGraphics|getGraphics)\s*\(",
        "Graphics resources must be disposed on all paths.",
        "Verify dispose() is called in finally.",
    ),
    Rule(
        "raw-inputstream",
        "P2",
        "Resource lifecycle",
        r"\.getInputStream\s*\(",
        "InputStream acquisition needs lifecycle review.",
        "Use try-with-resources or verify the callee closes it.",
    ),
    Rule(
        "fileinputstream",
        "P2",
        "Resource lifecycle",
        r"new\s+FileInputStream\s*\(",
        "FileInputStream must close on success and exception.",
        "Use try-with-resources or close in finally.",
    ),
    Rule(
        "multipart-large",
        "P2",
        "Config",
        r"spring\.servlet\.multipart\.(max-file-size|max-request-size)\s*=\s*(?:[1-9]\d{3,}MB|[2-9]GB|\d{10,})",
        "Large multipart limits increase temp-disk and request blast radius.",
        "Route large uploads to direct/chunk upload or lower regular multipart limits.",
    ),
    Rule(
        "multipart-tmp",
        "P2",
        "Config",
        r"spring\.servlet\.multipart\.location\s*=\s*/tmp\b",
        "Multipart temp files use /tmp, which may be ephemeral or capacity-limited.",
        "Use an explicitly mounted temp directory with quota and cleanup.",
    ),
    Rule(
        "heap-ratio",
        "P3",
        "JVM",
        r"MaxRAMPercentage\s*=\s*(?:6\d|7\d|8\d|9\d|100)(?:\.0)?",
        "High heap percentage can squeeze native memory in containers.",
        "Verify RSS headroom for direct memory, metaspace, threads, agents, and mmap.",
    ),
]


def iter_files(root: Path, extensions: Iterable[str]) -> Iterable[Path]:
    extensions = set(extensions)
    for current_root, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if d not in EXCLUDED_DIRS]
        for name in files:
            path = Path(current_root) / name
            if path.suffix in extensions:
                yield path


def scan_file(path: Path, root: Path) -> List[Finding]:
    findings: List[Finding] = []
    try:
        lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()
    except OSError:
        return findings

    rel = str(path.relative_to(root))
    for idx, line in enumerate(lines, start=1):
        stripped = line.strip()
        if not stripped or stripped.startswith("//") or stripped.startswith("# "):
            continue
        for rule in RULES:
            if re.search(rule.pattern, line):
                findings.append(
                    Finding(
                        severity=rule.severity,
                        category=rule.category,
                        rule_id=rule.rule_id,
                        path=rel,
                        line=idx,
                        snippet=stripped[:240],
                        message=rule.message,
                        recommendation=rule.recommendation,
                    )
                )
    return findings


def severity_key(finding: Finding) -> int:
    order = {"P0": 0, "P1": 1, "P2": 2, "P3": 3}
    return order.get(finding.severity, 9)


def print_markdown(findings: List[Finding], root: Path) -> None:
    print(f"# OOM Risk Scan\n\nRoot: `{root}`\n")
    if not findings:
        print("No configured OOM risk patterns found.")
        return

    counts = {}
    for finding in findings:
        counts[finding.severity] = counts.get(finding.severity, 0) + 1
    summary = ", ".join(f"{sev}: {counts[sev]}" for sev in sorted(counts))
    print(f"Summary: {summary}\n")

    for finding in sorted(findings, key=lambda f: (severity_key(f), f.path, f.line, f.rule_id)):
        print(f"- {finding.severity} `{finding.path}:{finding.line}` [{finding.category}/{finding.rule_id}]")
        print(f"  - Evidence: `{finding.snippet}`")
        print(f"  - Risk: {finding.message}")
        print(f"  - Check: {finding.recommendation}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Scan source files for common OOM risk patterns.")
    parser.add_argument("root", nargs="?", default=".", help="Repository or module path to scan.")
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of Markdown.")
    parser.add_argument(
        "--ext",
        action="append",
        default=[],
        help="Additional file extension to scan, such as .groovy. Can be repeated.",
    )
    args = parser.parse_args()

    root = Path(args.root).resolve()
    extensions = set(DEFAULT_EXTENSIONS)
    extensions.update(args.ext)

    findings: List[Finding] = []
    for path in iter_files(root, extensions):
        findings.extend(scan_file(path, root))

    findings.sort(key=lambda f: (severity_key(f), f.path, f.line, f.rule_id))

    if args.json:
        print(json.dumps([asdict(f) for f in findings], ensure_ascii=False, indent=2))
    else:
        print_markdown(findings, root)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
