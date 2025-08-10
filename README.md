# **DocuMind**

*Your Intelligent Research Paper Assistant — Powered by RAG & MLOps*

![CI/CD](https://github.com/knight22-21/documind/actions/workflows/ci-cd.yaml/badge.svg)
![License](https://img.shields.io/github/license/knight22-21/documind)
![Built with FastAPI](https://img.shields.io/badge/Built%20with-FastAPI-009688)
![Deployed on Render](https://img.shields.io/badge/Deployed-Render-6E44FF)

## **Overview**

**DocuMind** is an open-source, full-stack AI assistant designed to make working with research papers effortless.
It leverages a **Retrieval-Augmented Generation (RAG)** pipeline to combine **semantic search** with **LLM-based reasoning**, enabling accurate, context-rich responses with proper citations.

Built with **MLOps best practices** from day one, DocuMind ensures **testable, modular, and deployable code** — making it a strong foundation for AI-powered document analysis tools.

## Live Demo

Try it here: [documind.app](https://rag-research-paper.onrender.com)

## **Key Features**

✅ **PDF Upload & Parsing** — Extracts text from uploaded PDFs.
✅ **arXiv Integration** — Search & retrieve research papers by keywords.
✅ **RAG Pipeline** — Chunking, embeddings, vector storage, and semantic retrieval.
✅ **Groq API + Mixtral LLM** — Fast, low-latency inference with no local model hosting.
✅ **Qdrant Vector Database** — Open-source, high-performance vector storage.
✅ **MLOps CI/CD** — Automated testing, linting, coverage reports, and GitHub Actions pipeline.
✅ **Modular Architecture** — Clear separation of frontend, backend, and core logic.
✅ **Free & Open Source Stack** — No paid APIs (except optional LLM use).


## **Architecture**

```plaintext

├── .github/workflows/ci-cd.yaml      # CI/CD pipeline
├── backend/                          # Backend (FastAPI)
│   ├── api/routes/                   # API endpoints
│   ├── core/                         # Configs & constants
│   ├── rag/                          # RAG pipeline components
│   ├── services/                     # PDF parsing, arXiv, LLM
│   ├── tests/                        # Pytest suite
│   └── main.py                       # App entry point
├── frontend/                         # Frontend (HTML, CSS, JS)
├── Dockerfile                        # Containerization
├── .pre-commit-config.yaml           # Linting hooks
├── requirements.txt                  # Dependencies
└── requirements-dev.txt              # Dev/test dependencies
```

---

## **RAG Workflow**

1. **Upload PDF** or **search arXiv**.
2. **Text Extraction** → `pdf_reader.py`
3. **Chunking** → `chunker.py` (semantic chunks)
4. **Embedding** → `embedder.py` (SentenceTransformers)
5. **Vector Storage** → `qdrant_client.py`
6. **Semantic Retrieval** → `retriever.py`
7. **LLM Querying** → `llm_interface.py` (Groq API)
8. **Final Response** with citations.

---

## **MLOps Practices**

* **Pre-commit Hooks** — Auto-formatting & lint checks (`black`, `flake8`, `isort`).
* **Test Automation** — Pytest-based suite with high coverage.
* **Coverage Reports** — `pytest-cov` generates coverage reports, visible in CI.
* **GitHub Actions CI/CD** — Runs tests, lint, and coverage before deployment.
* **Modular Codebase** — Separation of concerns for scalability & maintainability.
* **Dockerized Environment** — Reproducible builds & deployments.

---

## **Tech Stack**

* **Backend:** FastAPI
* **Frontend:** HTML, CSS, JavaScript
* **Vector DB:** Qdrant
* **Embeddings:** SentenceTransformers
* **LLM:** Groq API
* **CI/CD:** GitHub Actions + pytest + pre-commit
* **Containerization:** Docker
* **Testing:** pytest, pytest-cov

---

## **Installation**

```bash
git clone https://github.com/knight22-21/documind.git
cd documind
pip install -r requirements.txt
```

## Environment Variables

Create a `.env` file in the root with the following keys:

```env
GROQ_API_KEY=your_groq_key
QDRANT_URL=https://your-qdrant-instance
QDRANT_API_KEY=your_qdrant_key
HF_API_KEY=your_huggingface_key
```

---

## **Run Locally**

```bash
uvicorn backend.main:app --reload
```

Then open `http://127.0.0.1:8000`.

---

## **Run with Docker**

```bash
docker build -t documind .
docker run -p 8000:8000 documind
```

---

## **Testing & Coverage**

```bash
pytest --cov=backend --cov-report=term-missing
```

---


## **License**

MIT License © 2025 Krishna

