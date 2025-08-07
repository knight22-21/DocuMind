from fastapi import APIRouter
from qdrant_client import QdrantClient

router = APIRouter()
client = QdrantClient(host="localhost", port=6333)

@router.get("/debug/qdrant/points")
def debug_qdrant(limit: int = 5):
    response = client.scroll(
        collection_name="research_papers",
        limit=limit,
        with_payload=True,
        with_vectors=False
    )
    return {
        "points": [point.dict() for point in response[0]]
    }
