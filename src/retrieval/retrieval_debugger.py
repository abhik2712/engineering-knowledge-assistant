# Pretty-print retrieval results so you can inspect quality manually.

from src.retrieval.models import RetrievalResult


def print_results(
    query: str,
    results: list[RetrievalResult],
    title: str,
    max_preview_chars: int = 500,
) -> None:
    print("\n" + "=" * 120)
    print(title)
    print(f"Query: {query}")
    print("=" * 120)

    if not results:
        print("No results found.")
        return

    for result in results:
        metadata = result.metadata or {}

        print("-" * 120)
        print(f"Rank: {result.rank}")
        print(f"Score: {result.score:.6f}")
        print(f"Retriever: {result.retriever}")
        print(f"Chunk ID: {result.chunk_id}")
        print(f"Source Type: {result.source_type}")
        print(f"Path: {result.path}")

        if metadata.get("section"):
            print(f"Section: {metadata.get('section')}")

        if metadata.get("component"):
            print(f"Component: {metadata.get('component')}")

        if metadata.get("severity"):
            print(f"Severity: {metadata.get('severity')}")

        fusion = metadata.get("fusion")
        if fusion:
            print(f"Fusion Method: {fusion.get('method')}")
            print(f"RRF Score: {fusion.get('rrf_score'):.6f}")
            print(f"Contributing Retrievers: {fusion.get('retrievers')}")

        preview = result.content[:max_preview_chars].replace("\n", " ")
        print(f"Preview: {preview}")