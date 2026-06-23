# Read data/metadata/chunks.jsonl and return chunks as Python dictionaries.
import json
from pathlib import Path
from typing import Any


def load_chunks(chunks_path: str) -> list[dict[str, Any]]:
    path = Path(chunks_path)

    if not path.exists():
        raise FileNotFoundError(f"Chunks file not found: {chunks_path}")

    chunks: list[dict[str, Any]] = []

    with path.open("r", encoding="utf-8") as f:
        for line_number, line in enumerate(f, start=1):
            line = line.strip()

            if not line:
                continue

            try:
                chunk = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(
                    f"Invalid JSON at line {line_number} in {chunks_path}: {exc}"
                ) from exc

            required_fields = ["chunk_id", "doc_id", "source_type", "path", "content"]
            missing_fields = [field for field in required_fields if field not in chunk]

            if missing_fields:
                raise ValueError(
                    f"Chunk at line {line_number} is missing fields: {missing_fields}"
                )

            chunks.append(chunk)

    return chunks

