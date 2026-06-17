# Step 4: Implement Source-Aware Chunking
# Create one entry function: def chunk_document(doc: RawDocument) -> list[ChunkDocument]:
# It should route based on source type:

# design_doc → markdown section chunking
# incident → markdown section chunking
# log → grouped log chunking
# code → line-range chunking
# metadata/json → skip for now or chunk simply

# 6.1 Markdown Section Chunking
# design doc
# incident

# Logic:
# - Split content by markdown headers (e.g., #, ##, ###)
# - keep headings and section content together

# Expected chunk examples:

# INC-001::section_0 → Summary
# INC-001::section_1 → Affected Component
# INC-001::section_2 → Timeline
# INC-001::section_3 → Root Cause

from pyclbr import Function

from .models import RawDocument, ChunkDocument


def chunk_markdown_by_sections(doc: RawDocument) -> list[ChunkDocument]:
    chunks = []
    lines = doc.content.splitlines()

    current_heading = "Document"
    current_lines = []
    chunk_index = 0

    def flush_section():
        nonlocal chunk_index, current_lines, current_heading

        text = "\n".join(current_lines).strip()
        if not text:
            return

        chunk_id = f"{doc.doc_id}::section_{chunk_index}"

        metadata = {
            **doc.metadata,
            "section": current_heading,
            "chunk_strategy": "markdown_section",
        }

        chunks.append(
            ChunkDocument(
                chunk_id=chunk_id,
                doc_id=doc.doc_id,
                source_type=doc.source_type,
                path=doc.path,
                content=text,
                metadata=metadata,
            )
        )

        chunk_index += 1

    for line in lines:
        if line.startswith("#"):
            flush_section()
            current_heading = line.lstrip("#").strip()
            current_lines = [line]
        else:
            current_lines.append(line)

    flush_section()
    return chunks

# 6.2 Log Group Chunking

# Logic: Group every 5 log lines into one chunk
# Later you can improve it using timestamp windows or incident IDs.
# Expected result:

# scrape_timeout.log::log_group_0
# scrape_timeout.log::log_group_1
# remote_write_backpressure.log::log_group_0
def chunk_logs(doc: RawDocument, group_size: int = 5) -> list[ChunkDocument]:
    chunks = []
    lines = [line for line in doc.content.splitlines() if line.strip()]

    for i in range(0, len(lines), group_size):
        group = lines[i : i + group_size]
        content = "\n".join(group)

        chunk_id = f"{doc.doc_id}::log_group_{i // group_size}"

        metadata = {
            **doc.metadata,
            "chunk_strategy": "log_group",
            "start_line": i + 1,
            "end_line": i + len(group),
        }

        chunks.append(
            ChunkDocument(
                chunk_id=chunk_id,
                doc_id=doc.doc_id,
                source_type=doc.source_type,
                path=doc.path,
                content=content,
                metadata=metadata,
            )
        )

    return chunks

# 6.3 Code Line-Range Chunking
# Logic - 
# For Day 4, use line-range chunks.

# Recommended size:

# 80 lines per chunk
# 20 lines overlap

# Why overlap?

# Because a function may start near the end of one chunk and continue into the next.

def chunk_code_by_lines(
    doc: RawDocument,
    chunk_size: int = 80,
    overlap: int = 20,
) -> list[ChunkDocument]:
    chunks = []
    lines = doc.content.splitlines()

    if not lines:
        return chunks

    start = 0
    chunk_index = 0

    while start < len(lines):
        end = min(start + chunk_size, len(lines))
        content = "\n".join(lines[start:end])

        chunk_id = f"{doc.doc_id}::code_{chunk_index}"

        metadata = {
            **doc.metadata,
            "chunk_strategy": "code_line_range",
            "language": "go",
            "start_line": start + 1,
            "end_line": end,
        }

        chunks.append(
            ChunkDocument(
                chunk_id=chunk_id,
                doc_id=doc.doc_id,
                source_type=doc.source_type,
                path=doc.path,
                content=content,
                metadata=metadata,
            )
        )

        chunk_index += 1

        if end == len(lines):
            break

        start = end - overlap

    return chunks

# 6.4 Router Function

def chunk_document(doc: RawDocument) -> list[ChunkDocument]:
    if doc.source_type in {"design_doc", "incident"}:
        return chunk_markdown_by_sections(doc)

    if doc.source_type == "log":
        return chunk_logs(doc)

    if doc.source_type == "code":
        return chunk_code_by_lines(doc)

    return []