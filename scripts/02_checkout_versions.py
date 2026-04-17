from __future__ import annotations

import argparse
from pathlib import Path

from common import ensure_command_exists, read_json, run_command, slugify_bug, write_json


def main() -> None:
    parser = argparse.ArgumentParser(description="Checkout buggy and fixed versions for selected BugsInPy bugs.")
    parser.add_argument(
        "--selected-bugs",
        type=Path,
        default=Path("outputs/selection/selected_bugs.json"),
        help="Path to selected_bugs.json",
    )
    parser.add_argument(
        "--workspace-dir",
        type=Path,
        default=Path("workspace/checkouts"),
        help="Where to create per-bug checkouts",
    )
    parser.add_argument(
        "--buggy-version-flag",
        type=str,
        default="0",
        help="Value to pass to bugsinpy-checkout -v for the buggy version",
    )
    parser.add_argument(
        "--fixed-version-flag",
        type=str,
        default="1",
        help="Value to pass to bugsinpy-checkout -v for the fixed version",
    )
    args = parser.parse_args()

    ensure_command_exists("bugsinpy-checkout.cmd")

    selected = read_json(args.selected_bugs)
    manifest = []

    for row in selected:
        project = row["project"]
        bug_id = str(row["bug_id"])
        slug = slugify_bug(project, bug_id)
        root = args.workspace_dir / slug
        buggy_dir = root / "buggy"
        fixed_dir = root / "fixed"
        root.mkdir(parents=True, exist_ok=True)

        item = {
            "project": project,
            "bug_id": bug_id,
            "slug": slug,
            "buggy_dir": str(buggy_dir.resolve()),
            "fixed_dir": str(fixed_dir.resolve()),
            "buggy_checkout_ok": False,
            "fixed_checkout_ok": False,
            "errors": [],
        }

        for version_flag, target_dir, label in [
            (args.buggy_version_flag, buggy_dir, "buggy"),
            (args.fixed_version_flag, fixed_dir, "fixed"),
        ]:
            target_dir.mkdir(parents=True, exist_ok=True)
            cmd = [
                "bugsinpy-checkout.cmd",
                "-p",
                project,
                "-i",
                bug_id,
                "-v",
                version_flag,
                "-w",
                target_dir.resolve().as_posix(),
            ]
            try:
                result = run_command(cmd, check=True)
                item[f"{label}_checkout_ok"] = True
                item[f"{label}_stdout"] = result.stdout[-4000:]
            except Exception as exc:
                item["errors"].append(f"{label}: {exc}")

        manifest.append(item)
        print(
            f"{project}-{bug_id}: buggy={'ok' if item['buggy_checkout_ok'] else 'fail'} | "
            f"fixed={'ok' if item['fixed_checkout_ok'] else 'fail'}"
        )

    out_path = Path("outputs/checkout_manifest.json")
    write_json(out_path, manifest)
    print(f"Wrote: {out_path}")


if __name__ == "__main__":
    main()
