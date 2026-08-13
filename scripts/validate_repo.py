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
    from build_tree import content_files, parse_front_matter

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
    records = {}
    current_ticker = None
    for line in text.splitlines():
        company_match = re.match(r"^    ([A-Z][A-Z0-9]*): \{$", line)
        if company_match:
            current_ticker = company_match.group(1)
            records[current_ticker] = {}
            continue
        if current_ticker:
            field_match = re.match(r'^      (updated|source): "([^"]+)"', line)
            if field_match:
                records[current_ticker][field_match.group(1)] = field_match.group(2)

    if not records:
        fail("research-state.js contains no decision sources")
    incomplete = [ticker for ticker, record in records.items() if not {"updated", "source"} <= record.keys()]
    if incomplete:
        fail("research state is missing updated/source fields for: " + ", ".join(incomplete))

    public_files = content_files()
    covered_tickers = {
        metadata.get("ticker")
        for public_path in public_files
        for metadata, _ in [parse_front_matter(public_path)]
        if metadata.get("ticker")
    }
    missing_state = sorted(covered_tickers - records.keys())
    if missing_state:
        fail("research state is missing covered tickers: " + ", ".join(missing_state))

    source_paths = [record["source"] for record in records.values()]
    missing = [source for source in source_paths if not (ROOT / source).exists()]
    if missing:
        fail("research state points to missing sources: " + ", ".join(missing))

    invalid_dates = []
    for value in (record["updated"] for record in records.values()):
        try:
            date.fromisoformat(value)
        except ValueError:
            invalid_dates.append(value)
    if invalid_dates:
        fail("research state contains invalid update dates: " + ", ".join(invalid_dates))

    for ticker, record in records.items():
        source_metadata, _ = parse_front_matter(ROOT / record["source"])
        if source_metadata.get("ticker") != ticker:
            fail(f"{ticker} decision source has mismatched ticker: {record['source']}")
        source_date = source_metadata.get("date")
        if source_date and record["updated"] < source_date:
            fail(f"{ticker} decision state predates its source report")

    decision_updates = {}
    for public_path in public_files:
        metadata, _ = parse_front_matter(public_path)
        if str(metadata.get("decision_update", "false")).lower() != "true":
            continue
        ticker = metadata.get("ticker")
        if not ticker:
            fail(f"decision_update report has no ticker: {public_path}")
        entry = (metadata.get("date", ""), str(public_path.relative_to(ROOT)))
        if ticker not in decision_updates or entry > decision_updates[ticker]:
            decision_updates[ticker] = entry

    for ticker, (report_date, report_path) in decision_updates.items():
        record = records.get(ticker)
        if not record:
            fail(f"decision update has no research state entry: {ticker}")
        if report_date > record["updated"]:
            fail(f"{ticker} conclusion is stale; update research-state.js for {report_path}")
        if record["source"] != report_path:
            fail(f"{ticker} decision source must point to latest decision update: {report_path}")

    as_of_match = re.search(r'\basOf:\s*"([^"]+)"', text)
    if not as_of_match:
        fail("research-state.js is missing asOf")
    as_of = as_of_match.group(1)
    try:
        date.fromisoformat(as_of)
    except ValueError:
        fail(f"research-state.js has invalid asOf date: {as_of}")
    latest_state_date = max(record["updated"] for record in records.values())
    if as_of < latest_state_date:
        fail("research-state.js asOf predates a company decision update")

    print(f"OK: decision layer checked for {len(records)} covered companies")


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


def check_frontend_syntax() -> None:
    if not shutil.which("node"):
        print("SKIP: Node.js unavailable; frontend syntax not checked")
        return
    index_path = ROOT / "index.html"
    text = index_path.read_text(encoding="utf-8")
    module_match = re.search(r'<script type="module">\s*(.*?)\s*</script>', text, re.DOTALL)
    if not module_match:
        fail("index.html is missing its module script")
    result = subprocess.run(
        ["node", "--check", "-"],
        input=module_match.group(1),
        capture_output=True,
        text=True,
    )
    if result.returncode:
        fail("index.html JavaScript syntax check failed: " + result.stderr.strip())
    required_views = {"showWelcome", "showOverview", "showCatalysts", "showLibrary", "showCompany", "showFinancialDashboard"}
    missing_views = sorted(name for name in required_views if f"function {name}" not in module_match.group(1))
    if missing_views:
        fail("index.html is missing workspace views: " + ", ".join(missing_views))
    print("OK: frontend syntax and workspace views checked")


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
    check_frontend_syntax()
    check_python_syntax()
    check_tracked_virtualenv()
    check_data_manifest()
    print("Repository validation passed.")
