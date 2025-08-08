from fastapi import APIRouter, Query
from backend.services.arxiv_search import search_arxiv
from fastapi import Request
from pydantic import BaseModel
import requests
from pathlib import Path
from backend.services.pdf_reader import extract_text_from_pdf
from backend.rag.chunker import chunk_text
from backend.rag.embedder import Embedder
from backend.rag.qdrant_client import init_collection, add_documents

router = APIRouter()

class DownloadRequest(BaseModel):
    url: str

@router.post("/arxiv/download")
def download_and_process(req: DownloadRequest):
    pdf_url = req.url
    filename = pdf_url.split("/")[-1]

    upload_dir = Path("backend") / "uploads"
    upload_dir.mkdir(parents=True, exist_ok=True) 

    file_path = upload_dir / filename

    # Download PDF
    response = requests.get(pdf_url)
    with open(file_path, "wb") as f:
        f.write(response.content)

    # Process PDF
    text = extract_text_from_pdf(str(file_path))
    chunks = chunk_text(text)
    embedder = Embedder()
    embeddings = embedder.encode(chunks)

    init_collection(dim=len(embeddings[0]))
    add_documents(chunks, embeddings, metadata={"source": filename})

    return {"filename": filename, "chunks": len(chunks)}




@router.get("/arxiv")
def arxiv_search(q: str = Query(...)):
    return {"results": search_arxiv(q)}
