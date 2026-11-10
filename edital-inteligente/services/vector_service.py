import hashlib
import chromadb
from services.embedding_service import embed_texts, embed_query

CHROMA_PATH = "./chroma_db"
_client = chromadb.PersistentClient(path=CHROMA_PATH)


def _collection_name(pdf_bytes: bytes) -> str:
    digest = hashlib.sha256(pdf_bytes).hexdigest()[:16]
    return f"edital_{digest}"


def index_document(filename: str, pdf_bytes: bytes, chunks: list[dict]) -> tuple[str, int]:
    """Cria uma coleção por arquivo; evita reindexar o mesmo PDF."""
    doc_id = _collection_name(pdf_bytes)
    collection = _client.get_or_create_collection(
        name=doc_id,
        metadata={"hnsw:space": "cosine", "filename": filename},
    )

    if collection.count() == 0:
        batch_size = 32
        for start in range(0, len(chunks), batch_size):
            batch = chunks[start:start + batch_size]
            texts = [item["text"] for item in batch]
            embeddings = embed_texts(texts)
            ids = [f"chunk_{start + i}" for i in range(len(batch))]
            metadatas = [
                {"page": item["page"], "filename": filename}
                for item in batch
            ]
            collection.add(
                ids=ids,
                documents=texts,
                embeddings=embeddings,
                metadatas=metadatas,
            )

    return doc_id, collection.count()


def search_document(doc_id: str, question: str, n_results: int = 5) -> list[dict]:
    collection = _client.get_collection(name=doc_id)
    total = collection.count()
    if total == 0:
        return []

    query_embedding = embed_query(question)
    result = collection.query(
        query_embeddings=[query_embedding],
        n_results=min(n_results, total),
        include=["documents", "metadatas", "distances"],
    )

    found = []
    for text, metadata, distance in zip(
        result["documents"][0],
        result["metadatas"][0],
        result["distances"][0],
    ):
        found.append({
            "text": text,
            "page": metadata["page"],
            "distance": float(distance),
        })
    return found
