#Convert each chunk to richer text before embedding.
# Instead of embedding only this:
# The scrape request failed because the target exceeded scrape_timeout...
# We embed this:
# Source Type: incident
# Component: scrape_manager
# Section: Root Cause
# Path: data/incidents/INC-001-scrape-timeout.md
# Content:
# The scrape request failed because the target exceeded scrape_timeout...

from typing import Any


def build_searchable_text(chunk: dict[str, Any]) -> str:
    metadata = chunk.get("metadata", {}) or {}

    parts = []

    parts.append(f"Source Type: {chunk.get('source_type', '')}")
    parts.append(f"Path: {chunk.get('path', '')}")

    title = metadata.get("title")
    if title:
        parts.append(f"Title: {title}")

    source_id = metadata.get("source_id")
    if source_id:
        parts.append(f"Source ID: {source_id}")

    component = metadata.get("component") or metadata.get("affected_component")
    if component:
        parts.append(f"Component: {component}")

    section = metadata.get("section")
    if section:
        parts.append(f"Section: {section}")

    severity = metadata.get("severity")
    if severity:
        parts.append(f"Severity: {severity}")

    tags = metadata.get("tags")
    if tags:
        if isinstance(tags, list):
            parts.append(f"Tags: {', '.join(tags)}")
        else:
            parts.append(f"Tags: {tags}")

    if metadata.get("start_line") and metadata.get("end_line"):
        parts.append(
            f"Line Range: {metadata.get('start_line')}-{metadata.get('end_line')}"
        )

    content = chunk.get("content", "")
    parts.append("\nContent:")
    parts.append(content)

    return "\n".join(parts)