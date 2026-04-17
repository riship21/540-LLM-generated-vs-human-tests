from __future__ import annotations

import argparse
from pathlib import Path

from common import extract_python_test_functions, read_json, slugify_bug, write_json


def locate_repo_root(checkout_parent: Path) -> Path:
    candidates = [p for p in checkout_parent.iterdir() if p.is_dir()]
    if len(candidates) == 1:
        return candidates[0]
    return checkout_parent


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract human-written test metadata from changed test files.")
    parser.add_argument(
        "--per-bug-dir",
        type=Path,
        default=Path("outputs/per_bug_json"),
        help="Directory with per-bug JSON files from step 03",
    )
    parser.add_argument(
        "--checkout-manifest",
        type=Path,
        default=Path("outputs/checkout_manifest.json"),
        help="Checkout manifest from step 02",
    )
    args = parser.parse_args()

    manifest = {}
    if args.checkout_manifest.exists():
        for item in read_json(args.checkout_manifest):
            manifest[(item["project"], str(item["bug_id"]))] = item

    for json_path in sorted(args.per_bug_dir.glob("*.json")):
        record = read_json(json_path)
        key = (record["project"], str(record["bug_id"]))
        checkout = manifest.get(key, {})

        fixed_parent = Path(checkout["fixed_dir"]) if checkout.get("fixed_dir") else None
        fixed_repo_root = locate_repo_root(fixed_parent) if fixed_parent and fixed_parent.exists() else None

        human_tests = []
        for file_entry in record.get("test_files", []):
            path_in_repo = file_entry.get("display_path") or file_entry.get("new_path") or file_entry.get("old_path")
            file_record = {
                "file": path_in_repo,
                "change_type": file_entry.get("change_type"),
                "added_test_defs": file_entry.get("added_test_defs", []),
                "deleted_test_defs": file_entry.get("deleted_test_defs", []),
                "added_assertions": file_entry.get("added_assertions", []),
                "extracted_functions": [],
            }

            if fixed_repo_root and path_in_repo:
                fixed_path = fixed_repo_root / path_in_repo
                function_map = extract_python_test_functions(fixed_path)
                for test_name in file_entry.get("added_test_defs", []):
                    if test_name in function_map:
                        file_record["extracted_functions"].append(function_map[test_name])

            human_tests.append(file_record)

        record["human_tests"] = human_tests
        record["human_test_names"] = sorted(
            {
                test_name
                for test_file in human_tests
                for test_name in test_file.get("added_test_defs", [])
            }
        )
        record["human_test_files"] = [t["file"] for t in human_tests]
        record["human_test_count"] = len(record["human_test_names"])
        write_json(json_path, record)
        print(f"Enriched test metadata for {slugify_bug(record['project'], record['bug_id'])}")


if __name__ == "__main__":
    main()
