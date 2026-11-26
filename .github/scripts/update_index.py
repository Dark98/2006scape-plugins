#!/usr/bin/env python3
"""Generate index.json from // @metadata headers in scripts/ and plugins/."""

import json
import os
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
INDEX_PATH = ROOT / "index.json"
SOURCE_DIRS = [("scripts", "script"), ("plugins", "plugin")]
SOURCE_EXTS = {".script", ".bsh", ".java"}


def slugify(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def parse_metadata(file_path: Path, default_type: str) -> dict:
    meta = {
        "id": "",
        "name": file_path.stem.replace("_", " "),
        "version": "1.0.0",
        "minApi": "1.0.0",
        "type": default_type,
        "author": "Anonymous",
        "description": "",
    }

    for raw_line in file_path.read_text(encoding="utf-8").splitlines():
        trimmed = raw_line.strip()
        if trimmed.startswith("//") or trimmed.startswith("#"):
            comment = trimmed[2:].strip() if trimmed.startswith("//") else trimmed[1:].strip()
            if comment.startswith("@id "):
                meta["id"] = comment[3:].strip()
            elif comment.startswith("@name "):
                meta["name"] = comment[5:].strip()
            elif comment.startswith("@author "):
                meta["author"] = comment[7:].strip()
            elif comment.startswith("@version "):
                meta["version"] = comment[8:].strip()
            elif comment.startswith("@minApi "):
                meta["minApi"] = comment[7:].strip()
            elif comment.startswith("@description "):
                meta["description"] = comment[12:].strip()
            elif comment.startswith("@desc "):
                meta["description"] = comment[5:].strip()
            elif comment.startswith("@type "):
                meta["type"] = comment[5:].strip().lower()
        elif trimmed:
            break

    if not meta["id"]:
        meta["id"] = slugify(meta["name"])
    return meta


def main() -> None:
    repo = os.environ.get("GITHUB_REPOSITORY", "dark98/2006scape-plugins")
    branch = os.environ.get("GITHUB_REF_NAME", "main")
    entries = []

    for dir_name, default_type in SOURCE_DIRS:
        folder = ROOT / dir_name
        if not folder.is_dir():
            continue
        for file_path in sorted(folder.iterdir(), key=lambda p: p.name.lower()):
            if not file_path.is_file() or file_path.suffix.lower() not in SOURCE_EXTS:
                continue
            meta = parse_metadata(file_path, default_type)
            rel_path = f"{dir_name}/{file_path.name}"
            entries.append({
                "id": meta["id"],
                "name": meta["name"],
                "version": meta["version"],
                "minApi": meta["minApi"],
                "type": meta["type"],
                "author": meta["author"],
                "description": meta["description"],
                "fileName": file_path.name,
                "downloadUrl": f"https://raw.githubusercontent.com/{repo}/{branch}/{rel_path}",
            })

    # Preserve any non-source entries (e.g. precompiled .jar / .dex) from existing index.json
    if INDEX_PATH.is_file():
        try:
            existing = json.loads(INDEX_PATH.read_text(encoding="utf-8"))
            seen_ids = {e["id"] for e in entries}
            for item in existing.get("plugins", []):
                fname = item.get("fileName", "")
                ext = Path(fname).suffix.lower()
                if ext not in SOURCE_EXTS and item.get("id") not in seen_ids:
                    entries.append(item)
        except Exception:
            pass

    output = {
        "schemaVersion": 1,
        "plugins": entries,
    }
    INDEX_PATH.write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
