# Orchestrate vector and BM25 index creation.
from .bm25_index import (
    build_bm25_index,
    save_bm25_chunk_store,
    save_bm25_index,
)
from .chunk_loader import load_chunks
from .embedding_model import EmbeddingModel
from .text_builder import build_searchable_text
from .vector_index import (
    build_faiss_index,
    save_chunk_store,
    save_faiss_index,
)


def build_indexes(
    chunks_path: str = "data/metadata/chunks.jsonl",
    vector_index_path: str = "data/indexes/vector/faiss.index",
    vector_chunk_store_path: str = "data/indexes/vector/chunk_store.jsonl",
    bm25_index_path: str = "data/indexes/bm25/bm25.pkl",
    bm25_chunk_store_path: str = "data/indexes/bm25/chunk_store.jsonl",
    embedding_model_name: str = "sentence-transformers/all-MiniLM-L6-v2",
) -> None:
    print("Loading chunks...")
    chunks = load_chunks(chunks_path)

    if not chunks:
        raise ValueError("No chunks found. Run ingestion before indexing.")

    print(f"Loaded chunks: {len(chunks)}")

    print("Building searchable texts...")
    searchable_texts = [build_searchable_text(chunk) for chunk in chunks]

    print("Loading embedding model...")
    embedding_model = EmbeddingModel(model_name=embedding_model_name)

    print("Generating embeddings...")
    embeddings = embedding_model.embed_texts(searchable_texts)

    print(f"Embedding shape: {embeddings.shape}")

    print("Building FAISS vector index...")
    faiss_index = build_faiss_index(embeddings)

    print("Saving FAISS index and chunk store...")
    save_faiss_index(faiss_index, vector_index_path)
    save_chunk_store(chunks, vector_chunk_store_path)

    print("Building BM25 index...")
    bm25_index = build_bm25_index(searchable_texts)

    print("Saving BM25 index and chunk store...")
    save_bm25_index(bm25_index, bm25_index_path)
    save_bm25_chunk_store(chunks, searchable_texts, bm25_chunk_store_path)

    print("Index build completed.")
    print(f"Vector index: {vector_index_path}")
    print(f"Vector chunk store: {vector_chunk_store_path}")
    print(f"BM25 index: {bm25_index_path}")
    print(f"BM25 chunk store: {bm25_chunk_store_path}")