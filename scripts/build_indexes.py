from pathlib import Path
import sys

# Ensure `src` is importable when running this file directly.
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.indexing.build_index import build_indexes


if __name__ == "__main__":
    build_indexes()
