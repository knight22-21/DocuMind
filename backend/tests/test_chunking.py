from backend.rag.chunker import chunk_text


def test_chunk_pdf_text():
    text = "This is a test. " * 50
    chunks = chunk_text(text, max_tokens=50)
    assert isinstance(chunks, list)
    assert all(isinstance(c, str) for c in chunks)
    assert len(chunks) > 1
