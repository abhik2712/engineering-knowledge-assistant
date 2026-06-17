# Step 3: Implement File Loading
# The loader should:

# 1.Walk through selected directories
# 2. Read supported files
# 3. Attach manifest metadata if available
# 4. Return RawDocument objects

from pathlib import Path
from typing import Any

from .models import RawDocument


SUPPORTED_EXTENSIONS = {".md", ".log", ".go", ".yaml", ".yml", ".json"}


def infer_source_type(path: str) -> str:
    if "/design_docs/" in path:
        return "design_doc"
    if "/incidents/" in path:
        return "incident"
    if "/logs/" in path:
        return "log"
    if "/code_repo/" in path:
        return "code"
    if "/metadata/" in path:
        return "metadata"
    return "unknown"


def load_documents(
    input_paths: list[str],
    manifest: dict[str, dict[str, Any]],
    project_root: str = ".",
) -> list[RawDocument]:
    root = Path(project_root)
    documents: list[RawDocument] = []

    for input_path in input_paths:
        base_path = root / input_path

        if not base_path.exists():
            print(f"Skipping missing path: {input_path}")
            continue

        files = [base_path] if base_path.is_file() else base_path.rglob("*")

        for file_path in files:
            if not file_path.is_file():
                continue

            if file_path.suffix not in SUPPORTED_EXTENSIONS:
                continue

            rel_path = str(file_path.relative_to(root))

            try:
                content = file_path.read_text(encoding="utf-8", errors="ignore")
            except Exception as exc:
                print(f"Failed to read {rel_path}: {exc}")
                continue

            manifest_metadata = manifest.get(rel_path)
            if manifest_metadata is None:
                for manifest_path, entry in manifest.items():
                    prefix = manifest_path.rstrip("/") + "/"
                    if rel_path.startswith(prefix):
                        manifest_metadata = entry
                        break
            if manifest_metadata is None:
                manifest_metadata = {}

            source_type = manifest_metadata.get("source_type") or infer_source_type(rel_path)

            doc_id = manifest_metadata.get("source_id") or rel_path.replace("/", "::")
            title = manifest_metadata.get("title") or file_path.name

            metadata = {
                **manifest_metadata,
                "extension": file_path.suffix,
                "filename": file_path.name,
            }

            documents.append(
                RawDocument(
                    doc_id=doc_id,
                    source_type=source_type,
                    path=rel_path,
                    title=title,
                    content=content,
                    metadata=metadata,
                )
            )

    return documents