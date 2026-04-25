from __future__ import annotations

import csv
import json
import shutil
from pathlib import Path

ROOT = Path(r"C:\open_source_eval")
OUT = ROOT / "benchmark_handoff"

TASKS = [
    {
        "slug": "slugify_basic",
        "repo": "python-slugify",
        "source_file": "slugify/slugify.py",
        "human_test_file": "test.py",
        "function": "slugify",
        "difficulty": "easy",
        "focus": "Basic slug generation from plain ASCII text.",
    },
    {
        "slug": "slugify_unicode",
        "repo": "python-slugify",
        "source_file": "slugify/slugify.py",
        "human_test_file": "test.py",
        "function": "slugify",
        "difficulty": "easy_medium",
        "focus": "Unicode handling and allow_unicode behavior.",
    },
    {
        "slug": "slugify_advanced",
        "repo": "python-slugify",
        "source_file": "slugify/slugify.py",
        "human_test_file": "test.py",
        "function": "slugify",
        "difficulty": "medium",
        "focus": "max_length, word_boundary, stopwords, replacements, separator.",
    },
    {
        "slug": "packaging_canonicalize_name",
        "repo": "packaging",
        "source_file": "src/packaging/utils.py",
        "human_test_file": "tests/test_utils.py",
        "function": "canonicalize_name",
        "difficulty": "easy",
        "focus": "Normalize Python package names consistently.",
    },
    {
        "slug": "packaging_is_normalized_name",
        "repo": "packaging",
        "source_file": "src/packaging/utils.py",
        "human_test_file": "tests/test_utils.py",
        "function": "is_normalized_name",
        "difficulty": "easy",
        "focus": "Detect whether a package name is already normalized.",
    },
    {
        "slug": "packaging_canonicalize_version",
        "repo": "packaging",
        "source_file": "src/packaging/utils.py",
        "human_test_file": "tests/test_utils.py",
        "function": "canonicalize_version",
        "difficulty": "medium",
        "focus": "Normalize version strings, including trailing zero behavior.",
    },
]

PROMPT_TEMPLATE = """You are given a Python function from an open-source project.

Task:
Write pytest unit tests for the target function only.

Rules:
- Generate only test code.
- Do not modify production code.
- Keep tests focused and minimal.
- Cover normal behavior and important edge cases.
- Follow pytest style.
- Do not look at the human baseline tests.

Repository: {repo}
Function: {function}
Difficulty: {difficulty}
Focus: {focus}

Deliverable:
Return only the test file content.
"""

def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)

    results_rows = []

    for task in TASKS:
        task_dir = OUT / task["slug"]
        source_dir = task_dir / "source"
        baseline_dir = task_dir / "human_baseline_locked"

        source_dir.mkdir(parents=True, exist_ok=True)
        baseline_dir.mkdir(parents=True, exist_ok=True)

        repo_root = ROOT / task["repo"]
        source_path = repo_root / task["source_file"]
        test_path = repo_root / task["human_test_file"]

        metadata = {
            "slug": task["slug"],
            "repo": task["repo"],
            "function": task["function"],
            "difficulty": task["difficulty"],
            "focus": task["focus"],
            "source_file": str(source_path),
            "human_test_file": str(test_path),
        }

        (task_dir / "metadata.json").write_text(
            json.dumps(metadata, indent=2), encoding="utf-8"
        )

        if source_path.exists():
            shutil.copy2(source_path, source_dir / source_path.name)

        if test_path.exists():
            shutil.copy2(test_path, baseline_dir / test_path.name)

        task_md = f"""# {task['slug']}

Repository: {task['repo']}
Function: {task['function']}
Difficulty: {task['difficulty']}

Goal:
{task['focus']}

Instructions for LLM teammate:
1. Read only the files in `source/` and `llm_prompt.txt` first.
2. Do NOT open `human_baseline_locked/` until after generating the LLM tests.
3. Save generated tests as `llm_generated_test.py`.
4. After generation, compare against the human baseline tests.
"""
        (task_dir / "task.md").write_text(task_md, encoding="utf-8")

        prompt = PROMPT_TEMPLATE.format(
            repo=task["repo"],
            function=task["function"],
            difficulty=task["difficulty"],
            focus=task["focus"],
        )
        (task_dir / "llm_prompt.txt").write_text(prompt, encoding="utf-8")

        results_rows.append({
            "slug": task["slug"],
            "repo": task["repo"],
            "function": task["function"],
            "difficulty": task["difficulty"],
            "llm_model": "",
            "prompt_type": "",
            "generated_test_file": "",
            "compiles": "",
            "runs": "",
            "passes_project_tests": "",
            "human_baseline_used": "yes",
            "notes": "",
        })

    with (OUT / "results_template.csv").open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "slug",
                "repo",
                "function",
                "difficulty",
                "llm_model",
                "prompt_type",
                "generated_test_file",
                "compiles",
                "runs",
                "passes_project_tests",
                "human_baseline_used",
                "notes",
            ],
        )
        writer.writeheader()
        writer.writerows(results_rows)

    print(f"Wrote handoff package to: {OUT}")

if __name__ == "__main__":
    main()