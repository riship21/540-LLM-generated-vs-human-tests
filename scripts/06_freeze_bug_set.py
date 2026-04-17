from __future__ import annotations

import argparse
import csv
from pathlib import Path

from common import read_json, write_csv, write_json


def read_summary_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def to_int(value: str | int | None) -> int:
    if value is None:
        return 0
    if isinstance(value, int):
        return value
    value = str(value).strip()
    if not value:
        return 0
    try:
        return int(value)
    except ValueError:
        return 0


def compact_join(items: list[str]) -> str:
    cleaned = [str(x).strip() for x in items if str(x).strip()]
    return "; ".join(cleaned)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Create a reviewable frozen bug set sheet with recommended keep/maybe/drop labels."
    )
    parser.add_argument(
        "--bug-summary",
        type=Path,
        default=Path("outputs/bug_summary.csv"),
        help="CSV produced by 05_build_summary.py",
    )
    parser.add_argument(
        "--per-bug-dir",
        type=Path,
        default=Path("outputs/per_bug_json"),
        help="Directory containing per-bug JSON files",
    )
    parser.add_argument(
        "--checkout-manifest",
        type=Path,
        default=Path("outputs/checkout_manifest.json"),
        help="Checkout manifest from step 02",
    )
    parser.add_argument(
        "--output-csv",
        type=Path,
        default=Path("outputs/frozen_bug_set.csv"),
        help="Reviewable frozen bug sheet",
    )
    parser.add_argument(
        "--output-json",
        type=Path,
        default=Path("outputs/frozen_bug_set.json"),
        help="JSON version of the same sheet",
    )
    parser.add_argument(
        "--max-files-changed",
        type=int,
        default=8,
        help="Recommended upper bound for a manageable bug patch",
    )
    args = parser.parse_args()

    summary_rows = read_summary_csv(args.bug_summary)
    manifest_items = read_json(args.checkout_manifest) if args.checkout_manifest.exists() else []
    manifest = {(item["project"], str(item["bug_id"])): item for item in manifest_items}

    per_bug = {}
    for path in sorted(args.per_bug_dir.glob("*.json")):
        record = read_json(path)
        per_bug[(record["project"], str(record["bug_id"]))] = record

    rows: list[dict[str, str | int | bool]] = []
    for row in summary_rows:
        key = (row["project"], str(row["bug_id"]))
        record = per_bug.get(key, {})
        checkout = manifest.get(key, {})

        files_changed = to_int(row.get("files_changed"))
        source_files_changed = to_int(row.get("source_files_changed"))
        test_files_changed = to_int(row.get("test_files_changed"))
        human_test_count = to_int(row.get("human_test_count"))
        buggy_ok = bool(checkout.get("buggy_checkout_ok"))
        fixed_ok = bool(checkout.get("fixed_checkout_ok"))
        checkout_ok = buggy_ok and fixed_ok
        manageable_patch = files_changed > 0 and files_changed <= args.max_files_changed
        has_source_diff = source_files_changed > 0
        has_test_context = test_files_changed > 0 or human_test_count > 0
        clear_bug_context = has_source_diff and manageable_patch
        usable_for_llm = checkout_ok and clear_bug_context and has_test_context

        reasons: list[str] = []
        if not checkout_ok:
            reasons.append("checkout failed")
        if not has_source_diff:
            reasons.append("no source diff")
        if not manageable_patch:
            reasons.append(f"patch too large ({files_changed} files)")
        if not has_test_context:
            reasons.append("weak human test context")

        if usable_for_llm:
            recommended_status = "keep"
        elif checkout_ok and clear_bug_context:
            recommended_status = "maybe"
        else:
            recommended_status = "drop"

        source_paths = [f.get("display_path") or f.get("new_path") or f.get("old_path") or "" for f in record.get("source_files", [])]
        test_paths = [f.get("display_path") or f.get("new_path") or f.get("old_path") or "" for f in record.get("test_files", [])]

        rows.append(
            {
                "project": row["project"],
                "bug_id": row["bug_id"],
                "slug": f"{row['project']}_{row['bug_id']}",
                "recommended_status": recommended_status,
                "status_final": recommended_status,
                "buggy_checkout_ok": buggy_ok,
                "fixed_checkout_ok": fixed_ok,
                "checkout_ok": checkout_ok,
                "files_changed": files_changed,
                "source_files_changed": source_files_changed,
                "test_files_changed": test_files_changed,
                "human_test_count": human_test_count,
                "human_test_names": row.get("human_test_names", ""),
                "human_test_files": row.get("human_test_files", ""),
                "source_file_paths": compact_join(source_paths),
                "test_file_paths": compact_join(test_paths),
                "clear_bug_context": clear_bug_context,
                "has_test_context": has_test_context,
                "usable_for_llm": usable_for_llm,
                "recommended_reason": "; ".join(reasons) if reasons else "ready for experiment",
                "review_notes": "",
                "patch_path": row.get("patch_path", ""),
                "buggy_commit": row.get("buggy_commit", ""),
                "fixed_commit": row.get("fixed_commit", ""),
                "failing_tests": row.get("failing_tests", ""),
            }
        )

    write_csv(args.output_csv, rows)
    write_json(args.output_json, rows)
    print(f"Wrote: {args.output_csv}")
    print(f"Wrote: {args.output_json}")
    keep_count = sum(1 for r in rows if r["recommended_status"] == "keep")
    maybe_count = sum(1 for r in rows if r["recommended_status"] == "maybe")
    drop_count = sum(1 for r in rows if r["recommended_status"] == "drop")
    print(f"Recommended keep={keep_count}, maybe={maybe_count}, drop={drop_count}")


if __name__ == "__main__":
    main()
