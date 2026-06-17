import json
from collections import Counter


CHUNKS_PATH = "data/metadata/chunks.jsonl"


def main():
    chunks = []

    with open(CHUNKS_PATH, "r", encoding="utf-8") as f:
        for line in f:
            chunks.append(json.loads(line))

    print(f"Total chunks: {len(chunks)}")

    source_type_counts = Counter(chunk["source_type"] for chunk in chunks)
    print("Chunks by source type:")
    for source_type, count in source_type_counts.items():
        print(f"  {source_type}: {count}")

    empty_chunks = [chunk for chunk in chunks if not chunk["content"].strip()]
    print(f"Empty chunks: {len(empty_chunks)}")

    missing_paths = [chunk for chunk in chunks if not chunk.get("path")]
    print(f"Chunks missing path: {len(missing_paths)}")

    missing_metadata = [chunk for chunk in chunks if not chunk.get("metadata")]
    print(f"Chunks missing metadata: {len(missing_metadata)}")

    print("\nSample chunks:")
    for chunk in chunks[:3]:
        print("-" * 80)
        print("chunk_id:", chunk["chunk_id"])
        print("source_type:", chunk["source_type"])
        print("path:", chunk["path"])
        print("metadata:", chunk["metadata"])
        print("content preview:", chunk["content"][:300])


if __name__ == "__main__":
    main()
