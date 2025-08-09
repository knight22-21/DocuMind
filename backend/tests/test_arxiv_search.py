import pytest
from unittest.mock import patch

@pytest.mark.parametrize("query", ["machine learning", "deep learning"])
@patch("backend.services.arxiv_service.search_arxiv")
def test_arxiv_search(mock_search, client, query):
    mock_search.return_value = [
        {"title": "Sample Paper", "pdf_url": "https://arxiv.org/pdf/1234.5678.pdf"}
    ]
    response = client.get("/arxiv/search", params={"query": query})
    assert response.status_code == 200
    results = response.json()
    assert isinstance(results, list)
    assert "pdf_url" in results[0]
