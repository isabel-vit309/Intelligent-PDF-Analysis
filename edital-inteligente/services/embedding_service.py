import ollama

EMBEDDING_MODEL = "embeddinggemma"

def embed_texts(texts: list[str]) -> list[list[float]]:
    """Gera embeddings localmente pelo Ollama."""
    result = ollama.embed(model=EMBEDDING_MODEL, input=texts)
    return result["embeddings"]


def embed_query(text: str) -> list[float]:
    result = ollama.embed(model=EMBEDDING_MODEL, input=text)
    return result["embeddings"][0]
