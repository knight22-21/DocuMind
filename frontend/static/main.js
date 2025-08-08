const form = document.getElementById("uploadForm");
const output = document.getElementById("output");

form.onsubmit = async (e) => {
  e.preventDefault();
  const formData = new FormData(form);
  const res = await fetch("/api/upload", {
    method: "POST",
    body: formData
  });
  const data = await res.json();
  output.textContent = data.text_preview;

  const openLink = document.getElementById("open-pdf");
  openLink.href = data.pdf_url;
  document.getElementById("pdf-link-container").style.display = "block";
};

async function askQuery() {
  const query = document.getElementById("userQuery").value;
  const res = await fetch("/api/query", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ query })
  });
  const data = await res.json();
  document.getElementById("answerOutput").textContent =
    `Answer: ${data.answer}\n\nSources: ${data.sources.join(', ')}`;

  const list = document.getElementById("citationsList");
  list.innerHTML = "";
  data.citations.forEach(c => {
    const li = document.createElement("li");
    li.textContent = `[${c.score.toFixed(3)}] ${c.text.slice(0, 150)}... (source: ${c.source})`;
    list.appendChild(li);
  });
}

async function searchArxiv() {
  const query = document.getElementById("arxivInput").value;
  const res = await fetch(`/api/arxiv?q=${encodeURIComponent(query)}`);
  const data = await res.json();

  const list = document.getElementById("arxivResults");
  list.innerHTML = "";
  data.results.forEach(paper => {
    const li = document.createElement("li");
    li.innerHTML = `
      <b>${paper.title}</b><br>
      ${paper.summary}<br>
      <button onclick="addArxivPaper('${paper.pdf_url}')">Import</button>
      <hr>
    `;
    list.appendChild(li);
  });
}

async function addArxivPaper(pdfUrl) {
  const res = await fetch("/api/arxiv/download", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ url: pdfUrl })
  });
  const data = await res.json();

  alert("✅ Imported: " + data.filename + "\nChunks: " + data.chunks);

  const openLink = document.getElementById("open-pdf");
  openLink.href = data.pdf_url;
  document.getElementById("pdf-link-container").style.display = "block";
}
