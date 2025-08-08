from fastapi import APIRouter
from pydantic import BaseModel
from backend.rag.retriever import retrieve_relevant_chunks
from backend.services.llm_interface import generate_answer

router = APIRouter()

class QueryRequest(BaseModel):
    query: str

@router.post("/query")
def query_paper(request: QueryRequest):
    chunks = retrieve_relevant_chunks(request.query)

    if not chunks:
        return {"answer": "No relevant context found.", "sources": []}

    context_texts = [c["text"] for c in chunks]
    sources = [c["source"] for c in chunks]

    answer = generate_answer(request.query, context_texts)

    return {
        "answer": answer,
        "sources": list(set(sources)),
        "citations": chunks  # raw chunks: includes text, score, and source
    }