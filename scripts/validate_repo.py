#!/usr/bin/env python3
"""Validate generated navigation, local paths, and Python syntax."""

from __future__ import annotations

import ast
import json
import re
import shutil
import subprocess
import sys
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def check_tree_data() -> None:
    from build_tree import build_tree, generate_js, generate_search_js

    expected = generate_js(build_tree())
    actual_path = ROOT / "tree-data.js"
    if not actual_path.exists():
        fail("tree-data.js is missing; run python3 build_tree.py")
    if actual_path.read_text(encoding="utf-8") != expected:
        fail("tree-data.js is stale; run python3 build_tree.py")
    search_path = ROOT / "search-data.js"
    if not search_path.exists() or search_path.read_text(encoding="utf-8") != generate_search_js():
        fail("search-data.js is stale; run python3 build_tree.py")

    tree = build_tree()
    paths = []
    for category in tree.values():
        for group in category.values():
            paths.extend(item["path"] for item in group)
    missing = [path for path in paths if not (ROOT / path).exists()]
    if missing:
        fail("navigation contains missing paths: " + ", ".join(missing))
    print(f"OK: navigation contains {len(paths)} existing Markdown files")


def check_financial_data() -> None:
    path = ROOT / "financial-data.js"
    if not path.exists():
        fail("financial-data.js is missing")
    payload = path.read_text(encoding="utf-8").split("const FINANCIAL_DATA =", 1)[-1]
    payload = payload.rsplit(";", 1)[0].strip()
    try:
        data = json.loads(payload)
    except json.JSONDecodeError as exc:
        fail(f"financial-data.js is not valid JSON: {exc}")

    for ticker, rows in data.items():
        periods = [row.get("period") for row in rows]
        if len(periods) != len(set(periods)):
            fail(f"{ticker} contains duplicate financial periods")
        for row in rows:
            for key in ("_period_end", "_filing_date"):
                if row.get(key):
                    try:
                        date.fromisoformat(row[key])
                    except ValueError:
                        fail(f"{ticker} {row.get('period')} has invalid {key}: {row[key]}")
            source_paths = {row.get("_source_path", "")}
            source_paths.update(
                source.get("path", "")
                for source in row.get("_metric_sources", {}).values()
            )
            for source_path in filter(None, source_paths):
                if not (ROOT / source_path).exists():
                    fail(f"{ticker} {row.get('period')} points to missing source: {source_path}")
            for metric, value in row.items():
                if metric.startswith("_") or metric == "period":
                    continue
                if not isinstance(value, (int, float)):
                    fail(f"{ticker} {row.get('period')} has non-numeric {metric}")
    print(f"OK: financial provenance checked for {len(data)} tickers")


def check_research_state() -> None:
    path = ROOT / "research-state.js"
    if not path.exists():
        fail("research-state.js is missing")
    text = path.read_text(encoding="utf-8")
    if shutil.which("node"):
        result = subprocess.run(
            ["node", "--check", str(path)], capture_output=True, text=True
        )
        if result.returncode:
            fail("research-state.js syntax check failed: " + result.stderr.strip())
    source_paths = re.findall(r'\bsource:\s*"([^"]+)"', text)
    if not source_paths:
        fail("research-state.js contains no decision sources")
    missing = [source for source in source_paths if not (ROOT / source).exists()]
    if missing:
        fail("research state points to missing sources: " + ", ".join(missing))
    invalid_dates = []
    for value in re.findall(r'\bupdated:\s*"([^"]+)"', text):
        try:
            date.fromisoformat(value)
        except ValueError:
            invalid_dates.append(value)
    if invalid_dates:
        fail("research state contains invalid update dates: " + ", ".join(invalid_dates))
    print(f"OK: decision layer checked for {len(source_paths)} covered companies")


def check_metadata() -> None:
    from build_tree import content_files, parse_front_matter

    required = {"schema_version", "title", "date", "type"}
    missing = []
    for path in content_files():
        metadata, _ = parse_front_matter(path)
        absent = sorted(required - metadata.keys())
        if absent:
            missing.append(f"{path}: {', '.join(absent)}")
    if missing:
        fail("Markdown metadata is incomplete: " + "; ".join(missing))
    print(f"OK: metadata checked for {len(content_files())} public Markdown files")


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


def check_data_manifest() -> None:
    path = ROOT / "data-manifest.json"
    if not path.exists():
        fail("data-manifest.json is missing; run python3 scripts/build_data_manifest.py")
    try:
        manifest = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        fail(f"data-manifest.json is not valid JSON: {exc}")
    entries = manifest.get("files", [])
    if manifest.get("file_count") != len(entries):
        fail("data-manifest.json file_count does not match files")
    missing = [item.get("path") for item in entries if not (ROOT / item.get("path", "")).exists()]
    if missing:
        fail("data manifest contains missing files: " + ", ".join(missing[:5]))
    print(f"OK: data manifest covers {len(entries)} existing files")


if __name__ == "__main__":
    check_tree_data()
    check_metadata()
    check_research_state()
    check_financial_data()
    check_python_syntax()
    check_tracked_virtualenv()
    check_data_manifest()
    print("Repository validation passed.")
