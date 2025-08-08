import requests
import xml.etree.ElementTree as ET

def search_arxiv(query: str, max_results=3):
    url = f"http://export.arxiv.org/api/query?search_query=all:{query}&start=0&max_results={max_results}"
    response = requests.get(url)
    root = ET.fromstring(response.content)

    ns = {'atom': 'http://www.w3.org/2005/Atom'}
    results = []

    for entry in root.findall('atom:entry', ns):
        title = entry.find('atom:title', ns).text.strip()
        summary = entry.find('atom:summary', ns).text.strip()
        
        # FIXED: Safely access 'title' attribute using .get()
        pdf_link = next(
            (l.attrib['href'] for l in entry.findall('atom:link', ns) if l.attrib.get('title') == 'pdf'),
            None
        )

        results.append({
            "title": title,
            "summary": summary,
            "pdf_url": pdf_link
        })

    return results
