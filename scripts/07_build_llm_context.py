from __future__ import annotations

import argparse
import csv
import json
import re
from pathlib import Path
from typing import Any

from common import read_json, safe_read_text, write_json

HUNK_RE = re.compile(r"@@\s+-(\d+)(?:,(\d+))?\s+\+(\d+)(?:,(\d+))?\s+@@")
TEST_NAME_RE = re.compile(r"(?:(?:^|::)(test_[A-Za-z0-9_]+))")

MIN_PROMPT_TEMPLATE = """You are given a real historical bug from a Python project.

Your task is to generate a unit test that would expose the bug in the buggy version.

Rules:
- Generate only test code.
- Follow the repository's existing test style.
- Do not modify production code.
- Focus on a minimal regression test.
- Reuse naming, imports, fixtures, and assertion style from nearby human-written tests when helpful.

Project: {project}
Bug ID: {bug_id}
Slug: {slug}

Bug overview:
{bug_overview}

Relevant buggy source context:
{buggy_source_focus}

Failing / related test context:
{failing_test_focus}

Repository test style notes:
{repo_style_notes}
"""

ENHANCED_PROMPT_TEMPLATE = """You are given a real historical bug from a Python project.

Your task is to generate a unit test that would expose the bug in the buggy version.

Rules:
- Generate only test code.
- Follow the repository's existing test style.
- Do not modify production code.
- Focus on a minimal regression test.
- Reuse naming, imports, fixtures, and assertion style from nearby human-written tests when helpful.

Project: {project}
Bug ID: {bug_id}
Slug: {slug}

Bug overview:
{bug_overview}

Relevant buggy source context:
{buggy_source_focus}

Failing / related test context:
{failing_test_focus}

Repository test style notes:
{repo_style_notes}

Bug-fix patch:
{patch_text}
"""


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def locate_repo_root(checkout_parent: Path | None) -> Path | None:
    if not checkout_parent or not checkout_parent.exists():
        return None
    candidates = [p for p in checkout_parent.iterdir() if p.is_dir()]
    if len(candidates) == 1:
        return candidates[0]
    return checkout_parent


def parse_hunk_header(header: str) -> tuple[int, int, int, int] | None:
    m = HUNK_RE.search(header)
    if not m:
        return None
    old_start = int(m.group(1))
    old_len = int(m.group(2) or "1")
    new_start = int(m.group(3))
    new_len = int(m.group(4) or "1")
    return old_start, old_len, new_start, new_len


def numbered_window(text: str, start_line: int, line_count: int, window: int = 30) -> str:
    lines = text.splitlines()
    if not lines:
        return ""
    start_idx = max(start_line - 1 - window, 0)
    end_idx = min(start_line - 1 + max(line_count, 1) + window, len(lines))
    return "\n".join(f"{i+1}: {lines[i]}" for i in range(start_idx, end_idx))


def numbered_head(text: str, max_lines: int = 250) -> str:
    lines = text.splitlines()[:max_lines]
    return "\n".join(f"{i+1}: {line}" for i, line in enumerate(lines))


def extract_function_names_from_failing_tests(failing_tests: str) -> list[str]:
    names = []
    for part in re.split(r"[;,\n]+", failing_tests or ""):
        m = TEST_NAME_RE.search(part.strip())
        if m:
            names.append(m.group(1))
    return list(dict.fromkeys(names))


def find_test_file_in_repo(repo_root: Path | None, failing_tests: str) -> Path | None:
    if not repo_root:
        return None
    for part in re.split(r"[;,\n]+", failing_tests or ""):
        piece = part.strip().replace("\\", "/")
        if not piece:
            continue
        # direct repo-relative path
        if ".py" in piece:
            path_part = piece.split("::", 1)[0]
            candidate = repo_root / path_part
            if candidate.exists():
                return candidate
            # last resort: suffix match
            matches = list(repo_root.rglob(Path(path_part).name))
            if matches:
                return matches[0]
    return None


def extract_named_test_blocks(text: str, target_names: list[str], context_lines: int = 8) -> str:
    if not text.strip():
        return ""
    lines = text.splitlines()
    targets = set(target_names)
    results: list[str] = []
    i = 0
    while i < len(lines):
        line = lines[i]
        match = re.match(r"^(\s*)def\s+(test_[A-Za-z0-9_]+)\s*\(", line)
        if not match:
            i += 1
            continue
        indent = len(match.group(1))
        name = match.group(2)
        if targets and name not in targets:
            i += 1
            continue
        start = max(i - context_lines, 0)
        j = i + 1
        while j < len(lines):
            next_line = lines[j]
            if next_line.strip() and (len(next_line) - len(next_line.lstrip())) <= indent and re.match(r"^\s*(def|class)\s+", next_line):
                break
            j += 1
        block = "\n".join(f"{k+1}: {lines[k]}" for k in range(start, j))
        results.append(f"### TEST BLOCK: {name}\n{block}")
        i = j
    return "\n\n".join(results)


def build_buggy_source_context(record: dict[str, Any], buggy_repo_root: Path | None) -> tuple[str, dict[str, str]]:
    sections: list[str] = []
    full_files: dict[str, str] = {}
    if not buggy_repo_root:
        return "(buggy checkout not available)", full_files

    for file_entry in record.get("source_files", []):
        path_in_repo = file_entry.get("display_path") or file_entry.get("old_path") or file_entry.get("new_path")
        if not path_in_repo:
            continue
        full_path = buggy_repo_root / path_in_repo
        if not full_path.exists() or full_path.suffix != ".py":
            continue
        text = safe_read_text(full_path)
        full_files[path_in_repo] = text
        file_sections: list[str] = []
        for hunk in file_entry.get("hunks", []):
            parsed = parse_hunk_header(hunk.get("header", ""))
            if not parsed:
                continue
            old_start, old_len, _, _ = parsed
            file_sections.append(numbered_window(text, old_start, old_len, window=35))
        if not file_sections:
            file_sections = [numbered_head(text, max_lines=250)]
        deduped: list[str] = []
        seen = set()
        for sec in file_sections:
            key = sec.strip()
            if key and key not in seen:
                deduped.append(sec)
                seen.add(key)
        sections.append(f"### FILE: {path_in_repo}\n" + "\n\n".join(deduped[:3]))
    return ("\n\n".join(sections) if sections else "(no Python source context extracted)"), full_files


def build_failing_test_context(record: dict[str, Any], row: dict[str, str], fixed_repo_root: Path | None, buggy_repo_root: Path | None) -> tuple[str, str, dict[str, str], list[str]]:
    failing_tests = row.get("failing_tests", "")
    target_names = extract_function_names_from_failing_tests(failing_tests)
    full_files: dict[str, str] = {}

    fixed_file = find_test_file_in_repo(fixed_repo_root, failing_tests)
    buggy_file = find_test_file_in_repo(buggy_repo_root, failing_tests)
    chosen = fixed_file or buggy_file

    focus_chunks: list[str] = []
    full_text = ""

    if chosen and chosen.exists() and chosen.suffix == ".py":
        full_text = safe_read_text(chosen)
        try:
            rel = str(chosen.relative_to(fixed_repo_root or buggy_repo_root or chosen.parent))
        except Exception:
            rel = chosen.name
        full_files[rel] = full_text
        named = extract_named_test_blocks(full_text, target_names)
        if named:
            focus_chunks.append(named)
        else:
            focus_chunks.append(f"### TEST FILE HEAD: {rel}\n{numbered_head(full_text, max_lines=250)}")

    # fallback to extracted human tests from record
    if not focus_chunks:
        for test_record in (record.get("human_tests", []) or [])[:3]:
            path_in_repo = test_record.get("file") or ""
            extracted = test_record.get("extracted_functions", []) or []
            if extracted:
                for fn in extracted[:4]:
                    qualname = fn.get("qualname") or fn.get("name") or "test"
                    body = fn.get("body") or ""
                    focus_chunks.append(f"### TEST: {qualname} ({path_in_repo})\n{body}")

    if not focus_chunks:
        for file_entry in record.get("test_files", [])[:2]:
            path_in_repo = file_entry.get("display_path") or file_entry.get("new_path") or file_entry.get("old_path")
            if not path_in_repo:
                continue
            repo_root = fixed_repo_root or buggy_repo_root
            if not repo_root:
                continue
            full_path = repo_root / path_in_repo
            if full_path.exists() and full_path.suffix == ".py":
                text = safe_read_text(full_path)
                full_files[path_in_repo] = text
                focus_chunks.append(f"### TEST FILE: {path_in_repo}\n{numbered_head(text, max_lines=250)}")
                break

    focus_text = "\n\n".join(focus_chunks) if focus_chunks else "(no human/failing test context extracted)"
    return focus_text, full_text, full_files, target_names


def infer_repo_style_notes(test_focus: str, test_full: str, record: dict[str, Any]) -> str:
    notes: list[str] = []
    combined = f"{test_focus}\n{test_full}"
    if "self.assert" in combined:
        notes.append("Repository uses unittest-style assertions in at least some tests.")
    if "pytest" in combined or "assert " in combined:
        notes.append("Prefer pytest-style assertions when consistent with nearby examples.")
    if re.search(r"@pytest\.mark", combined):
        notes.append("Nearby tests use pytest markers; preserve marker style if relevant.")
    if re.search(r"\bfixture\b", combined) or re.search(r"@pytest\.fixture", combined):
        notes.append("Reuse existing fixtures/helpers instead of building heavy setup from scratch.")
    if any("tests/" in (p.get("display_path") or "").replace("\\", "/") for p in record.get("test_files", [])):
        notes.append("Keep generated tests in the repository's existing tests/ layout.")
    notes.append("Generate only test code, not explanations.")
    notes.append("Prefer a focused regression test that targets the changed behavior.")
    notes.append("Do not modify production code, build scripts, or fixtures unless the repository style clearly requires a local helper.")
    return "\n".join(f"- {note}" for note in notes)


def keep_row(row: dict[str, str], include_maybe: bool) -> bool:
    status = (row.get("status_final") or row.get("recommended_status") or "").strip().lower()
    return status == "keep" or (include_maybe and status == "maybe")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def write_overview(path: Path, row: dict[str, str], record: dict[str, Any], metadata: dict[str, Any]) -> None:
    source_paths = metadata.get("source_file_paths", [])
    test_paths = metadata.get("test_file_paths", [])
    text = f"""Project: {row['project']}
Bug: {metadata['slug']}
Bug ID: {row['bug_id']}

Changed source file(s):
- """ + "\n- ".join(source_paths or ["(none)"]) + """

Changed test file(s):
- """ + "\n- ".join(test_paths or ["(none captured in patch)"]) + f"""

Known failing test reference(s):
{row.get('failing_tests', '(none listed)')}

Why selected:
- buggy and fixed checkouts are available
- patch metadata was extracted successfully
- bug is narrow enough for focused unit test generation
- source/test context is packaged for LLM prompting

Task for model:
Generate a regression-style unit test that fails on the buggy version.
Follow repository test style.
Do not change source code.
"""
    write_text(path, text)


def write_execution_notes(path: Path, metadata: dict[str, Any], row: dict[str, str]) -> None:
    text = f"""Execution notes for team members
================================

Project: {metadata['project']}
Bug ID: {metadata['bug_id']}
Slug: {metadata['slug']}

Buggy checkout path:
{metadata.get('buggy_checkout_path', '')}

Fixed checkout path:
{metadata.get('fixed_checkout_path', '')}

Known failing test reference(s):
{metadata.get('failing_tests', '')}

Changed source file(s):
- """ + "\n- ".join(metadata.get("source_file_paths", []) or ["(none)"]) + """

Changed test file(s):
- """ + "\n- ".join(metadata.get("test_file_paths", []) or ["(none)"]) + f"""

Commits:
- Buggy commit: {metadata.get('buggy_commit', '')}
- Fixed commit: {metadata.get('fixed_commit', '')}

Recommended usage:
1. Use llm_prompt_minimal.txt for a fairer baseline.
2. Use llm_prompt_enhanced.txt for richer context / RAG-style prompting.
3. Run generated tests against the buggy checkout first.
4. Check whether the same test passes or is no longer failing on the fixed checkout.
"""
    write_text(path, text)


def main() -> None:
    parser = argparse.ArgumentParser(description="Build rich LLM context packages per frozen bug.")
    parser.add_argument("--frozen-bugs", type=Path, default=Path("outputs/frozen_bug_set.csv"))
    parser.add_argument("--per-bug-dir", type=Path, default=Path("outputs/per_bug_json"))
    parser.add_argument("--checkout-manifest", type=Path, default=Path("outputs/checkout_manifest.json"))
    parser.add_argument("--output-dir", type=Path, default=Path("llm_context"))
    parser.add_argument("--include-maybe", action="store_true")
    args = parser.parse_args()

    frozen_rows = read_csv_rows(args.frozen_bugs)
    per_bug: dict[tuple[str, str], dict[str, Any]] = {}
    for path in sorted(args.per_bug_dir.glob("*.json")):
        record = read_json(path)
        per_bug[(record["project"], str(record["bug_id"]))] = record

    manifest_items = read_json(args.checkout_manifest) if args.checkout_manifest.exists() else []
    manifest = {(item["project"], str(item["bug_id"])): item for item in manifest_items}

    args.output_dir.mkdir(parents=True, exist_ok=True)

    kept = 0
    package_rows: list[dict[str, Any]] = []
    for row in frozen_rows:
        if not keep_row(row, include_maybe=args.include_maybe):
            continue

        key = (row["project"], str(row["bug_id"]))
        record = per_bug.get(key)
        checkout = manifest.get(key, {})
        if not record:
            print(f"Skipping {row['project']}_{row['bug_id']}: missing per-bug JSON")
            continue

        slug = record.get("slug") or f"{row['project']}_{row['bug_id']}"
        out_dir = args.output_dir / slug
        out_dir.mkdir(parents=True, exist_ok=True)

        buggy_repo_root = locate_repo_root(Path(checkout["buggy_dir"])) if checkout.get("buggy_dir") else None
        fixed_repo_root = locate_repo_root(Path(checkout["fixed_dir"])) if checkout.get("fixed_dir") else None

        patch_text = safe_read_text(Path(record["patch_path"])) if record.get("patch_path") else ""
        buggy_source_focus, buggy_source_files = build_buggy_source_context(record, buggy_repo_root)
        failing_test_focus, failing_test_full_text, failing_test_files, failing_test_names = build_failing_test_context(
            record, row, fixed_repo_root, buggy_repo_root
        )
        repo_style_notes = infer_repo_style_notes(failing_test_focus, failing_test_full_text, record)

        metadata = {
            "project": row["project"],
            "bug_id": str(row["bug_id"]),
            "slug": slug,
            "status_final": row.get("status_final", row.get("recommended_status", "")),
            "recommended_status": row.get("recommended_status", ""),
            "buggy_checkout_path": checkout.get("buggy_dir", ""),
            "fixed_checkout_path": checkout.get("fixed_dir", ""),
            "source_files_changed": record.get("source_files_changed", 0),
            "test_files_changed": record.get("test_files_changed", 0),
            "human_test_names": record.get("human_test_names", []),
            "human_test_files": record.get("human_test_files", []),
            "source_file_paths": [
                f.get("display_path") or f.get("old_path") or f.get("new_path")
                for f in record.get("source_files", [])
            ],
            "test_file_paths": [
                f.get("display_path") or f.get("old_path") or f.get("new_path")
                for f in record.get("test_files", [])
            ],
            "failing_tests": row.get("failing_tests", ""),
            "failing_test_names": failing_test_names,
            "buggy_commit": row.get("buggy_commit", ""),
            "fixed_commit": row.get("fixed_commit", ""),
            "context_level": "rich",
        }

        write_json(out_dir / "metadata.json", metadata)
        write_text(out_dir / "fix_patch.diff", patch_text)
        write_text(out_dir / "buggy_source_focus.txt", buggy_source_focus)
        write_text(out_dir / "failing_test_focus.txt", failing_test_focus)
        write_text(out_dir / "repo_style_notes.txt", repo_style_notes)
        write_overview(out_dir / "bug_overview.md", row, record, metadata)
        write_execution_notes(out_dir / "execution_notes.md", metadata, row)

        # full source files
        source_full_dir = out_dir / "buggy_source_full"
        for rel_path, text in buggy_source_files.items():
            write_text(source_full_dir / rel_path, text)

        # full failing / related test files
        test_full_dir = out_dir / "failing_test_full"
        for rel_path, text in failing_test_files.items():
            write_text(test_full_dir / rel_path, text)

        # human-only notes placeholder
        human_notes = f"""Human review notes
==================

Slug: {slug}

Why selected:
- checkout succeeded
- patch extracted
- source context available
- failing or related test context available

Open questions / reviewer notes:
- Add any ambiguity about bug scope here.
- Add any special execution caveats here.
- Note whether the failing test file is very broad or nicely localized.
"""
        write_text(out_dir / "human_notes_only.md", human_notes)

        minimal_prompt = MIN_PROMPT_TEMPLATE.format(
            project=row["project"],
            bug_id=row["bug_id"],
            slug=slug,
            bug_overview=safe_read_text(out_dir / "bug_overview.md"),
            buggy_source_focus=buggy_source_focus,
            failing_test_focus=failing_test_focus,
            repo_style_notes=repo_style_notes,
        )
        write_text(out_dir / "llm_prompt_minimal.txt", minimal_prompt)

        enhanced_prompt = ENHANCED_PROMPT_TEMPLATE.format(
            project=row["project"],
            bug_id=row["bug_id"],
            slug=slug,
            bug_overview=safe_read_text(out_dir / "bug_overview.md"),
            buggy_source_focus=buggy_source_focus,
            failing_test_focus=failing_test_focus,
            repo_style_notes=repo_style_notes,
            patch_text=patch_text,
        )
        write_text(out_dir / "llm_prompt_enhanced.txt", enhanced_prompt)

        kept += 1
        package_rows.append(
            {
                "slug": slug,
                "project": row["project"],
                "bug_id": str(row["bug_id"]),
                "dir": str(out_dir.resolve()),
                "status_final": metadata["status_final"],
            }
        )
        print(f"Built rich LLM context for {slug}")

    manifest_summary = {
        "kept_context_packages": kept,
        "output_dir": str(args.output_dir.resolve()),
        "packages": package_rows,
    }
    write_json(args.output_dir / "_manifest.json", manifest_summary)
    print(f"Wrote: {args.output_dir / '_manifest.json'}")


if __name__ == "__main__":
    main()
