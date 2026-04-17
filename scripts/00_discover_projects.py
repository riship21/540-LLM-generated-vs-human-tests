from __future__ import annotations

import argparse
from pathlib import Path

from common import list_bug_ids, list_projects, read_project_info, write_csv, write_json


def main() -> None:
    parser = argparse.ArgumentParser(description="Discover BugsInPy projects and bug counts.")
    parser.add_argument("--bugsinpy-root", required=True, type=Path, help="Path to local BugsInPy clone")
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("outputs/discovery"),
        help="Where to write discovery outputs",
    )
    args = parser.parse_args()

    projects = list_projects(args.bugsinpy_root)
    rows = []
    detailed = []

    for project in projects:
        bug_ids = list_bug_ids(args.bugsinpy_root, project)
        info = read_project_info(args.bugsinpy_root, project)
        repo_hint = info.get("github_url") or info.get("repo") or info.get("repository") or info.get("url")
        row = {
            "project": project,
            "bug_count": len(bug_ids),
            "first_bug_id": bug_ids[0] if bug_ids else "",
            "last_bug_id": bug_ids[-1] if bug_ids else "",
            "repo_hint": repo_hint or "",
        }
        rows.append(row)
        detailed.append({**row, "bug_ids": bug_ids, "project_info": info})

    args.output_dir.mkdir(parents=True, exist_ok=True)
    write_csv(args.output_dir / "projects.csv", rows)
    write_json(args.output_dir / "projects.json", detailed)

    print(f"Discovered {len(rows)} projects.")
    for row in rows:
        print(f"- {row['project']}: {row['bug_count']} bugs")
    print(f"Wrote: {args.output_dir / 'projects.csv'}")
    print(f"Wrote: {args.output_dir / 'projects.json'}")


if __name__ == "__main__":
    main()
