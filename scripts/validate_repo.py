#!/usr/bin/env python3
"""Validate generated navigation, local paths, and Python syntax."""

from __future__ import annotations

import ast
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def check_tree_data() -> None:
    from build_tree import build_tree, generate_js

    expected = generate_js(build_tree())
    actual_path = ROOT / "tree-data.js"
    if not actual_path.exists():
        fail("tree-data.js is missing; run python3 build_tree.py")
    if actual_path.read_text(encoding="utf-8") != expected:
        fail("tree-data.js is stale; run python3 build_tree.py")

    tree = build_tree()
    paths = []
    for category in tree.values():
        for group in category.values():
            paths.extend(item["path"] for item in group)
    missing = [path for path in paths if not (ROOT / path).exists()]
    if missing:
        fail("navigation contains missing paths: " + ", ".join(missing))
    print(f"OK: navigation contains {len(paths)} existing Markdown files")


def check_python_syntax() -> None:
    files = sorted(ROOT.rglob("*.py"))
    files = [
        path
        for path in files
        if not any(
            part in {"venv", "env"} or part.startswith(".venv-")
            for part in path.parts
        )
    ]
    for path in files:
        try:
            ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        except (OSError, SyntaxError) as exc:
            fail(f"Python syntax check failed for {path}: {exc}")
    print(f"OK: Python syntax checked for {len(files)} files")


def check_tracked_virtualenv() -> None:
    result = subprocess.run(
        ["git", "ls-files"], cwd=ROOT, check=True, capture_output=True, text=True
    )
    tracked = [line for line in result.stdout.splitlines() if ".venv" in Path(line).parts]
    if tracked:
        fail("virtual-environment files are tracked: " + ", ".join(tracked[:5]))
    print("OK: no virtual-environment files are tracked")


if __name__ == "__main__":
    check_tree_data()
    check_python_syntax()
    check_tracked_virtualenv()
    print("Repository validation passed.")
