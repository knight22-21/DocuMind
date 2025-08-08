from fastapi import APIRouter, Query
from backend.services.arxiv_search import search_arxiv

router = APIRouter()

@router.get("/arxiv")
def arxiv_search(q: str = Query(...)):
    return {"results": search_arxiv(q)}
