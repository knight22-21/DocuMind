def test_upload_valid_pdf(client, sample_pdf_file):
    response = client.post("/upload", files=sample_pdf_file)
    assert response.status_code == 200
    data = response.json()
    assert "file_id" in data


def test_upload_invalid_file(client):
    files = {"file": ("test.txt", b"Not a PDF", "text/plain")}
    response = client.post("/upload", files=files)
    assert response.status_code == 400
