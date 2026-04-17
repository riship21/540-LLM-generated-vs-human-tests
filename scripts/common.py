from __future__ import annotations

import ast
import csv
import json
import re
import shutil
import subprocess
from pathlib import Path
from typing import Any


TEST_PATH_PATTERNS = [
    re.compile(r"(^|/)tests?(/|$)", re.IGNORECASE),
    re.compile(r"(^|/)test_[^/]+\.py$", re.IGNORECASE),
    re.compile(r"(^|/)[^/]+_test\.py$", re.IGNORECASE),
]


def safe_read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="latin-1")


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows and not fieldnames:
        fieldnames = []
    elif fieldnames is None:
        ordered = []
        seen = set()
        for row in rows:
            for key in row.keys():
                if key not in seen:
                    seen.add(key)
                    ordered.append(key)
        fieldnames = ordered

    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames or [])
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def run_command(cmd: list[str], cwd: Path | None = None, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        cmd,
        cwd=str(cwd) if cwd else None,
        check=check,
        text=True,
        capture_output=True,
    )


def ensure_command_exists(name: str) -> None:
    if shutil.which(name) is None:
        raise SystemExit(
            f"Required command '{name}' was not found on PATH. "
            f"Install/configure it first, then rerun."
        )


def project_dir(bugsinpy_root: Path, project: str) -> Path:
    return bugsinpy_root / "projects" / project


def bug_dir(bugsinpy_root: Path, project: str, bug_id: str | int) -> Path:
    return project_dir(bugsinpy_root, project) / "bugs" / str(bug_id)


def list_projects(bugsinpy_root: Path) -> list[str]:
    base = bugsinpy_root / "projects"
    if not base.exists():
        raise FileNotFoundError(f"Could not find projects directory: {base}")
    return sorted([p.name for p in base.iterdir() if p.is_dir()])


def list_bug_ids(bugsinpy_root: Path, project: str) -> list[str]:
    base = project_dir(bugsinpy_root, project) / "bugs"
    if not base.exists():
        return []

    def sort_key(name: str) -> tuple[int, str]:
        return (0, f"{int(name):08d}") if name.isdigit() else (1, name)

    return sorted([p.name for p in base.iterdir() if p.is_dir()], key=sort_key)


def parse_key_value_text(text: str) -> dict[str, str]:
    result: dict[str, str] = {}
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" in line:
            key, value = line.split("=", 1)
        elif ":" in line:
            key, value = line.split(":", 1)
        else:
            continue
        result[key.strip()] = value.strip()
    return result


def read_project_info(bugsinpy_root: Path, project: str) -> dict[str, str]:
    path = project_dir(bugsinpy_root, project) / "project.info"
    return parse_key_value_text(safe_read_text(path)) if path.exists() else {}


def read_bug_info(bugsinpy_root: Path, project: str, bug_id: str | int) -> dict[str, str]:
    path = bug_dir(bugsinpy_root, project, bug_id) / "bug.info"
    return parse_key_value_text(safe_read_text(path)) if path.exists() else {}


def is_test_path(path: str) -> bool:
    normalized = path.replace("\\", "/")
    return any(pattern.search(normalized) for pattern in TEST_PATH_PATTERNS)


def normalize_diff_path(path: str) -> str:
    path = path.strip()
    if path.startswith("a/") or path.startswith("b/"):
        path = path[2:]
    return path


def parse_unified_diff(patch_text: str) -> list[dict[str, Any]]:
    files: list[dict[str, Any]] = []
    current: dict[str, Any] | None = None
    current_hunk: dict[str, Any] | None = None

    for line in patch_text.splitlines():
        if line.startswith("diff --git "):
            parts = line.split()
            old_path = normalize_diff_path(parts[2]) if len(parts) >= 4 else ""
            new_path = normalize_diff_path(parts[3]) if len(parts) >= 4 else old_path
            current = {
                "old_path": old_path,
                "new_path": new_path,
                "display_path": new_path or old_path,
                "change_type": "modified",
                "is_test_file": is_test_path(new_path or old_path),
                "added_lines": 0,
                "deleted_lines": 0,
                "added_assertions": [],
                "added_test_defs": [],
                "deleted_test_defs": [],
                "hunks": [],
            }
            current_hunk = None
            files.append(current)
            continue

        if current is None:
            continue

        if line.startswith("new file mode"):
            current["change_type"] = "added"
            continue
        if line.startswith("deleted file mode"):
            current["change_type"] = "deleted"
            continue
        if line.startswith("rename from "):
            current["rename_from"] = line.removeprefix("rename from ").strip()
            continue
        if line.startswith("rename to "):
            current["rename_to"] = line.removeprefix("rename to ").strip()
            continue
        if line.startswith("--- "):
            old_path = line[4:].strip()
            if old_path != "/dev/null":
                current["old_path"] = normalize_diff_path(old_path)
            continue
        if line.startswith("+++ "):
            new_path = line[4:].strip()
            if new_path != "/dev/null":
                current["new_path"] = normalize_diff_path(new_path)
                current["display_path"] = current["new_path"]
                current["is_test_file"] = is_test_path(current["display_path"])
            continue
        if line.startswith("@@"):
            current_hunk = {"header": line, "lines": []}
            current["hunks"].append(current_hunk)
            continue

        if current_hunk is not None:
            current_hunk["lines"].append(line)
            if line.startswith("+") and not line.startswith("+++"):
                current["added_lines"] += 1
                added_code = line[1:]
                stripped = added_code.strip()
                if stripped.startswith("assert") or "self.assert" in stripped or "pytest.raises" in stripped:
                    current["added_assertions"].append(stripped)
                test_def = extract_test_name_from_code_line(added_code)
                if test_def:
                    current["added_test_defs"].append(test_def)
            elif line.startswith("-") and not line.startswith("---"):
                current["deleted_lines"] += 1
                deleted_code = line[1:]
                test_def = extract_test_name_from_code_line(deleted_code)
                if test_def:
                    current["deleted_test_defs"].append(test_def)

    for file_entry in files:
        for key in ["added_assertions", "added_test_defs", "deleted_test_defs"]:
            file_entry[key] = sorted(set(file_entry[key]))
        file_entry["hunk_count"] = len(file_entry["hunks"])

    return files


def extract_test_name_from_code_line(code_line: str) -> str | None:
    match = re.match(r"\s*def\s+(test_[A-Za-z0-9_]+)\s*\(", code_line)
    if match:
        return match.group(1)
    return None


def extract_python_test_functions(file_path: Path) -> dict[str, dict[str, Any]]:
    if not file_path.exists() or file_path.suffix != ".py":
        return {}

    try:
        text = safe_read_text(file_path)
        tree = ast.parse(text)
    except (SyntaxError, ValueError):
        return {}

    lines = text.splitlines()
    result: dict[str, dict[str, Any]] = {}

    class Visitor(ast.NodeVisitor):
        def __init__(self) -> None:
            self.class_stack: list[str] = []

        def visit_ClassDef(self, node: ast.ClassDef) -> Any:
            self.class_stack.append(node.name)
            self.generic_visit(node)
            self.class_stack.pop()

        def visit_FunctionDef(self, node: ast.FunctionDef) -> Any:
            if node.name.startswith("test_"):
                start = getattr(node, "lineno", None)
                end = getattr(node, "end_lineno", None)
                body = ""
                if start is not None and end is not None:
                    body = "\n".join(lines[start - 1:end])
                qualname = ".".join(self.class_stack + [node.name]) if self.class_stack else node.name
                result[node.name] = {
                    "name": node.name,
                    "qualname": qualname,
                    "class_name": self.class_stack[-1] if self.class_stack else None,
                    "start_line": start,
                    "end_line": end,
                    "body": body,
                }
            self.generic_visit(node)

    Visitor().visit(tree)
    return result


def slugify_bug(project: str, bug_id: str | int) -> str:
    return f"{project}_{bug_id}".replace("/", "_")
