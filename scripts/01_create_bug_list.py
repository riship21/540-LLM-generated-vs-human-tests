from __future__ import annotations

import argparse
from pathlib import Path

from common import list_bug_ids, read_bug_info, read_project_info, write_csv, write_json


def main() -> None:
    parser = argparse.ArgumentParser(description="Create a selected bug list for mining.")
    parser.add_argument("--bugsinpy-root", required=True, type=Path, help="Path to local BugsInPy clone")
    parser.add_argument(
        "--projects",
        nargs="+",
        required=True,
        help="Project names to include, e.g. pandas ansible youtube-dl",
    )
    parser.add_argument(
        "--limit-per-project",
        type=int,
        default=5,
        help="How many bugs to take from each project",
    )
    parser.add_argument(
        "--start-from",
        type=int,
        default=1,
        help="1-based offset per project, useful if you want the 6th-10th bugs next",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("outputs/selection"),
        help="Where to write selection outputs",
    )
    args = parser.parse_args()

    rows = []
    start_index = max(args.start_from - 1, 0)

    for project in args.projects:
        project_info = read_project_info(args.bugsinpy_root, project)
        repo_hint = project_info.get("github_url") or project_info.get("repo") or project_info.get("repository") or project_info.get("url")
        bug_ids = list_bug_ids(args.bugsinpy_root, project)
        selected = bug_ids[start_index:start_index + args.limit_per_project]

        for bug_id in selected:
            bug_info = read_bug_info(args.bugsinpy_root, project, bug_id)
            rows.append(
                {
                    "project": project,
                    "bug_id": bug_id,
                    "repo_hint": repo_hint or "",
                    "buggy_commit": bug_info.get("buggy_commit_id") or bug_info.get("buggy_commit") or "",
                    "fixed_commit": bug_info.get("fixed_commit_id") or bug_info.get("fixed_commit") or "",
                    "python_version": bug_info.get("python_version") or "",
                    "status": "selected",
                    "notes": "",
                }
            )

    args.output_dir.mkdir(parents=True, exist_ok=True)
    write_csv(args.output_dir / "selected_bugs.csv", rows)
    write_json(args.output_dir / "selected_bugs.json", rows)

    print(f"Selected {len(rows)} bugs across {len(args.projects)} project(s).")
    print(f"Wrote: {args.output_dir / 'selected_bugs.csv'}")
    print(f"Wrote: {args.output_dir / 'selected_bugs.json'}")


if __name__ == "__main__":
    main()
