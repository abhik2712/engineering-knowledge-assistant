#Step 2: Load Source Manifest
#This file should read:data/metadata/source_manifest.json
# The goal is to map file paths to metadata.
# {
#   "source_id": "INC-001",
#   "source_type": "incident",
#   "path": "data/incidents/INC-001-scrape-timeout.md",
#   "title": "Scrape Timeout Incident",
#   "component": "scrape_manager",
#   "severity": "SEV-2",
#   "tags": ["scrape", "timeout"],
#   "linked_sources": [
#     "data/logs/scrape_timeout.log",
#     "data/design_docs/prometheus_scrape_lifecycle.md"
#   ]
# }

# Expected output : A dictionary mapping file paths to their corresponding metadata entries. For example:
# {
#   "data/incidents/INC-001-scrape-timeout.md": {
#     "source_id": "INC-001",
#     "source_type": "incident",
#     ...
#   }
# }

import json
from pathlib import Path
from typing import Any


def load_source_manifest(manifest_path: str) -> dict[str, dict[str, Any]]:
    path = Path(manifest_path)

    if not path.exists():
        return {}

    with path.open("r", encoding="utf-8") as f:
        payload = json.load(f)

    if isinstance(payload, dict):
        entries = payload.get("sources", [])
    elif isinstance(payload, list):
        entries = payload
    else:
        entries = []

    manifest = {}
    for entry in entries:
        if not isinstance(entry, dict):
            continue

        entry_path = entry.get("path")
        if not entry_path:
            continue

        normalized_entry = dict(entry)
        if "source_id" not in normalized_entry and "id" in normalized_entry:
            normalized_entry["source_id"] = normalized_entry["id"]
        if "source_type" not in normalized_entry and "type" in normalized_entry:
            normalized_entry["source_type"] = normalized_entry["type"]

        manifest[entry_path] = normalized_entry

    return manifest