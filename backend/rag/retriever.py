from qdrant_client import QdrantClient
from qdrant_client.http.models import SearchRequest, Filter, Payload, PayloadSelector
from backend.rag.embedder import Embedder

client = QdrantClient(host="localhost", port=6333)
embedder = Embedder()

def retrieve_relevant_chunks(query: str, top_k: int = 5) -> list[dict]:
    query_vector = embedder.encode([query])[0]

    hits = client.search(
        collection_name="research_papers",
        query_vector=query_vector,
        limit=top_k,
        with_payload=True
    )

    return [
        {
            "text": hit.payload["text"],
            "source": hit.payload["source"],
            "score": hit.score
        }
        for hit in hits
    ]
