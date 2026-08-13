#!/usr/bin/env python3
"""Build a reproducible manifest for tracked raw research files."""

from __future__ import annotations

import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "data-manifest.json"


def tracked_data_files() -> list[Path]:
    result = subprocess.run(
        ["git", "ls-files", "research/*/data/**"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return [ROOT / line for line in result.stdout.splitlines() if line]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    files = tracked_data_files()
    entries = []
    for path in files:
        if not path.exists():
            raise SystemExit(f"Missing tracked data file: {path}")
        entries.append({
            "path": str(path.relative_to(ROOT)),
            "size_bytes": path.stat().st_size,
            "sha256": sha256(path),
        })
    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "root": "research/*/data/",
        "file_count": len(entries),
        "total_bytes": sum(item["size_bytes"] for item in entries),
        "files": entries,
    }
    OUTPUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {OUTPUT}: {len(entries)} files")


if __name__ == "__main__":
    main()
