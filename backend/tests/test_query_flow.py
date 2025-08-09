from unittest.mock import patch

@patch("backend.rag.retriever.retrieve_relevant_chunks")
@patch("backend.services.llm_interface.generate_answer")
def test_query_with_results(mock_generate, mock_retrieve, client):
    mock_retrieve.return_value = [
        {"text": "Sample chunk text", "source": "paper1.pdf", "page": 2}
    ]
    mock_generate.return_value = "This is the answer."

    payload = {"query": "What is AI?"}
    response = client.post("/query", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data["answer"] == "This is the answer."
    assert "sources" in data

def test_query_no_results(client):
    with patch("backend.rag.retriever.retrieve_relevant_chunks", return_value=[]):
        payload = {"query": "Random question"}
        response = client.post("/query", json=payload)
        assert response.status_code == 200
        assert response.json()["answer"] == "No relevant context found."
