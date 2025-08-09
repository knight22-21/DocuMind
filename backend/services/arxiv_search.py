import requests
import xml.etree.ElementTree as ET


def search_arxiv(query: str, max_results: int = 3) -> list[dict]:
    url = (
        f"http://export.arxiv.org/api/query?search_query=all:{query}"
        f"&start=0&max_results={max_results}"
    )

    response = requests.get(url)
    response.raise_for_status()  # Add error handling

    root = ET.fromstring(response.content)

    ns = {"atom": "http://www.w3.org/2005/Atom"}
    results = []

    for entry in root.findall("atom:entry", ns):
        title = entry.find("atom:title", ns).text.strip()
        summary = entry.find("atom:summary", ns).text.strip()

        id_url = entry.find("atom:id", ns).text
        arxiv_id = id_url.split("/")[-1]

        pdf_url = next(
            (
                link.attrib["href"]
                for link in entry.findall("atom:link", ns)
                if link.attrib.get("title") == "pdf"
            ),
            f"https://arxiv.org/pdf/{arxiv_id}.pdf",
        )

        results.append(
            {
                "title": title,
                "summary": summary,
                "arxiv_id": arxiv_id,
                "pdf_url": pdf_url,
            }
        )

    return results
