from unittest.mock import patch


@patch("backend.rag.retriever.retrieve_relevant_chunks")
@patch("backend.services.llm_interface.generate_answer")
@patch("backend.services.embedder.Embedder.encode")
def test_query_with_results(mock_encode, mock_generate, mock_retrieve, client):
    mock_encode.return_value = [[0.1] * 384]
    mock_retrieve.return_value = [
        {"text": "Sample chunk text", "source": "paper1.pdf", "page": 2}
    ]
    mock_generate.return_value = "This is the answer."

    payload = {"query": "What is AI?"}
    response = client.post("/api/query", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data["answer"] == "This is the answer."
    assert "sources" in data


@patch("backend.services.llm_interface.generate_answer")
@patch("backend.rag.retriever.retrieve_relevant_chunks", return_value=[])
@patch("backend.services.embedder.Embedder.encode")
def test_query_no_results(mock_encode, mock_retrieve, mock_generate, client):
    mock_encode.return_value = [[0.1] * 384]
    mock_generate.return_value = "No relevant context found."

    payload = {"query": "Random question"}
    response = client.post("/api/query", json=payload)

    assert response.status_code == 200
    assert response.json()["answer"] == "No relevant context found."
