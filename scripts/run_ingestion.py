# Step 6: Add Runner Script
from pathlib import Path
import sys

# Ensure `src` is importable when running this file directly.
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.ingestion.pipeline import run_ingestion


if __name__ == "__main__":
    input_paths = [
        "data/design_docs",
        "data/logs",
        "data/incidents",

        # Start small for code.
        # Do not ingest full Prometheus repo yet.
        "data/code_repo/prometheus/scrape",
        "data/code_repo/prometheus/discovery",
        "data/code_repo/prometheus/rules",
        "data/code_repo/prometheus/storage",
    ]

    run_ingestion(input_paths=input_paths)