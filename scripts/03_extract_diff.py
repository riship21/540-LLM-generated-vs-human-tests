from __future__ import annotations

import argparse
import shutil
from pathlib import Path

from common import bug_dir, parse_unified_diff, read_bug_info, read_json, safe_read_text, slugify_bug, write_json


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract structured diff metadata from BugsInPy bug patches.")
    parser.add_argument("--bugsinpy-root", required=True, type=Path, help="Path to local BugsInPy clone")
    parser.add_argument(
        "--selected-bugs",
        type=Path,
        default=Path("outputs/selection/selected_bugs.json"),
        help="Path to selected_bugs.json",
    )
    parser.add_argument(
        "--patch-copy-dir",
        type=Path,
        default=Path("data/patches"),
        help="Where to copy patch files",
    )
    parser.add_argument(
        "--per-bug-dir",
        type=Path,
        default=Path("outputs/per_bug_json"),
        help="Where to write per-bug JSON",
    )
    args = parser.parse_args()

    selected = read_json(args.selected_bugs)
    args.patch_copy_dir.mkdir(parents=True, exist_ok=True)
    args.per_bug_dir.mkdir(parents=True, exist_ok=True)

    for row in selected:
        project = row["project"]
        bug_id = str(row["bug_id"])
        slug = slugify_bug(project, bug_id)
        patch_path = bug_dir(args.bugsinpy_root, project, bug_id) / "bug_patch.txt"
        bug_info = read_bug_info(args.bugsinpy_root, project, bug_id)

        if not patch_path.exists():
            print(f"Skipping {slug}: missing {patch_path}")
            continue

        patch_text = safe_read_text(patch_path)
        files = parse_unified_diff(patch_text)
        source_files = [f for f in files if not f["is_test_file"]]
        test_files = [f for f in files if f["is_test_file"]]

        copied_patch = args.patch_copy_dir / f"{slug}.patch"
        shutil.copyfile(patch_path, copied_patch)

        record = {
            "project": project,
            "bug_id": bug_id,
            "slug": slug,
            "bug_info": bug_info,
            "patch_path": str(copied_patch.resolve()),
            "files_changed": len(files),
            "source_files_changed": len(source_files),
            "test_files_changed": len(test_files),
            "human_test_added": any(f["change_type"] == "added" for f in test_files),
            "human_test_modified": any(f["change_type"] == "modified" for f in test_files),
            "source_files": source_files,
            "test_files": test_files,
            "all_files": files,
            "reproducible": None,
            "notes": "",
        }
        write_json(args.per_bug_dir / f"{slug}.json", record)
        print(f"Processed diff for {slug}")


if __name__ == "__main__":
    main()
