#!/usr/bin/env python3
"""Scan repo directories and generate navigation/search data for index.html.

Run: python3 build_tree.py

Auto-discovers:
- research/[TICKER]/*.md     → 个股研究 (grouped by ticker)
- notes/*/*.md               → 行业笔记 (subdirs with "日报" get their own category)
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).parent.resolve()


FRONT_MATTER_RE = re.compile(r"\A---\s*\n(.*?)\n---\s*(?:\n|$)", re.DOTALL)


def _scalar(value: str):
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
        return value[1:-1]
    return value


def parse_front_matter(filepath: Path) -> tuple[dict, str]:
    """Return simple YAML front matter and Markdown body.

    The repository only needs scalar metadata, so a small parser keeps the
    static-site build dependency-free. Files without front matter remain
    supported during migration.
    """
    text = filepath.read_text(encoding="utf-8")
    match = FRONT_MATTER_RE.match(text)
    if not match:
        return {}, text

    metadata = {}
    for line in match.group(1).splitlines():
        key, separator, value = line.partition(":")
        if separator and key.strip():
            metadata[key.strip()] = _scalar(value)
    return metadata, text[match.end():]


def extract_date_and_title(filepath: str, body: str | None = None) -> tuple:
    """Extract date (YYYY-MM-DD) and display title from filename.

    Patterns:
    1. 2026-07-11_PLTR_buyside-memo       → (2026-07-11, "PLTR buyside memo")
    2. 美股收盘日报_2026-07-10              → (2026-07-10, "美股收盘日报")
    3. 2026-07-12 bare date                → (2026-07-12, "2026-07-12 bare date")
    """
    stem = Path(filepath).stem

    # Pattern 1: date prefix  YYYY-MM-DD_...
    m = re.match(r"(\d{4}-\d{2}-\d{2})_(.+)", stem)
    if m:
        return m.group(1), m.group(2).replace("_", " ").replace("-", " ")

    # Pattern 2: prefix_date  suffix_YYYY-MM-DD
    m = re.match(r"(.+?)_(\d{4}-\d{2}-\d{2})$", stem)
    if m:
        return m.group(2), m.group(1).replace("_", " ").replace("-", " ")

    # Pattern 3: bare date somewhere in filename
    m = re.match(r"(\d{4}-\d{2}-\d{2})", stem)
    if m:
        return m.group(1), stem

    if body:
        heading = re.search(r"^#\s+(.+?)\s*$", body, flags=re.MULTILINE)
        if heading:
            return None, heading.group(1).strip()

    return None, stem.replace("_", " ").replace("-", " ")


def infer_type(filepath: Path, title: str) -> str:
    name = filepath.stem.lower()
    text = f"{name} {title.lower()}"
    for key in (
        "buyside-memo",
        "earnings-update",
        "earnings-call-chronicle",
        "investment-audit",
        "competitor-macro-analysis",
        "corporate-chronicle",
        "bayesian-intrinsic-growth-valuation",
        "bayesian-intrinsic-growth",
        "biography",
        "chronicle",
    ):
        if key in text:
            return key
    if "日报" in text:
        return "daily-report"
    if filepath.parts and "notes" in filepath.parts:
        return "sector-note"
    return "research-note"


def content_entry(filepath: Path, ticker: str | None = None) -> dict:
    metadata, body = parse_front_matter(filepath)
    fallback_date, fallback_title = extract_date_and_title(str(filepath), body)
    title = metadata.get("title") or fallback_title
    date = metadata.get("date") or metadata.get("as_of") or fallback_date
    entry = {
        "path": str(filepath.relative_to(ROOT)),
        "title": title,
        "date": date,
        "type": metadata.get("type") or infer_type(filepath, title),
        "schema_version": metadata.get("schema_version", "1"),
    }
    if ticker or metadata.get("ticker"):
        entry["ticker"] = metadata.get("ticker") or ticker
    return entry


def content_files() -> list[Path]:
    """Return public Markdown content, excluding source archives under data/."""
    files = []
    research_dir = ROOT / "research"
    if research_dir.exists():
        for ticker_dir in sorted(research_dir.iterdir()):
            if ticker_dir.is_dir() and not ticker_dir.name.startswith("."):
                files.extend(sorted(ticker_dir.glob("*.md")))

    notes_dir = ROOT / "notes"
    if notes_dir.exists():
        for sub in sorted(notes_dir.iterdir()):
            if sub.is_dir() and not sub.name.startswith("."):
                files.extend(sorted(sub.glob("*.md")))
    return files


def ticker_from_dir(dirname: str) -> str:
    return dirname.upper()


def sector_label(dirname: str) -> str:
    name_map = {
        "space": "太空产业",
        "semiconductor": "半导体",
        "ai": "人工智能",
        "energy": "能源",
        "biotech": "生物科技",
        "fintech": "金融科技",
    }
    return name_map.get(dirname, dirname)


def is_daily_report_dir(dirname: str) -> bool:
    return "日报" in dirname


def build_tree():
    tree = {}

    # ── 1. 个股研究：research/[TICKER]/*.md ──
    research_dir = ROOT / "research"
    if research_dir.exists():
        cat_label = "📊 个股研究"
        tree[cat_label] = {}
        for ticker_dir in sorted(research_dir.iterdir()):
            if not ticker_dir.is_dir() or ticker_dir.name.startswith("."):
                continue
            ticker = ticker_from_dir(ticker_dir.name)
            files = []
            for md in ticker_dir.glob("*.md"):
                files.append(content_entry(md, ticker))
            files.sort(key=lambda item: (item.get("date") or "", item["title"]), reverse=True)
            if files:
                tree[cat_label][ticker] = files

    # ── 2. 行业笔记 & 日报：notes/ 下自动发现所有子目录 ──
    notes_dir = ROOT / "notes"
    if notes_dir.exists():
        notes_cat = "📝 行业笔记"
        tree[notes_cat] = {}

        for sub in sorted(notes_dir.iterdir()):
            if not sub.is_dir() or sub.name.startswith("."):
                continue

            if is_daily_report_dir(sub.name):
                # Daily reports get their own top-level category, grouped by year-month
                report_cat = f"📰 {sub.name}"
                files_by_ym = {}
                for md in sub.glob("*.md"):
                    entry = content_entry(md)
                    date = entry["date"]
                    if date:
                        parts = date.split("-")
                        ym_key = f"{parts[0]}年{parts[1]}月"
                    else:
                        import datetime
                        mtime = datetime.datetime.fromtimestamp(md.stat().st_mtime)
                        ym_key = f"{mtime.year}年{mtime.month}月"
                    if ym_key not in files_by_ym:
                        files_by_ym[ym_key] = []
                    files_by_ym[ym_key].append(entry)
                for ym in sorted(files_by_ym.keys(), reverse=True):
                    files_by_ym[ym].sort(
                        key=lambda item: (item.get("date") or "", item["title"]),
                        reverse=True,
                    )
                    tree[report_cat] = tree.get(report_cat, {})
                    tree[report_cat][ym] = files_by_ym[ym]
            else:
                # Regular sector notes
                group_name = sector_label(sub.name)
                files = []
                for md in sub.glob("*.md"):
                    files.append(content_entry(md))
                files.sort(key=lambda item: (item.get("date") or "", item["title"]), reverse=True)
                if files:
                    tree[notes_cat][group_name] = files

        # Remove empty notes category
        if not tree[notes_cat]:
            del tree[notes_cat]

    return tree


def generate_js(tree: dict) -> str:
    js = "// Auto-generated by build_tree.py. Do not edit manually.\n"
    js += f"const TREE_DATA = {json.dumps(tree, ensure_ascii=False, indent=2)};\n"
    return js


def generate_search_js() -> str:
    docs = []
    for filepath in content_files():
        entry = content_entry(filepath)
        _, body = parse_front_matter(filepath)
        entry["text"] = body
        docs.append(entry)
    return (
        "// Auto-generated by build_tree.py. Do not edit manually.\n"
        f"const SEARCH_DATA = {json.dumps(docs, ensure_ascii=False, indent=2)};\n"
    )


def main():
    tree = build_tree()
    js = generate_js(tree)
    output_path = ROOT / "tree-data.js"
    output_path.write_text(js, encoding="utf-8")
    search_path = ROOT / "search-data.js"
    search_path.write_text(generate_search_js(), encoding="utf-8")

    count = 0
    for cat in tree.values():
        for files in cat.values():
            count += len(files)

    print(f"Generated tree-data.js: {count} files across {len(tree)} categories")
    for cat, groups in tree.items():
        cat_count = sum(len(f) for f in groups.values())
        print(f"  {cat}: {cat_count} files")

if __name__ == "__main__":
    main()
