const form = document.getElementById("uploadForm");
const output = document.getElementById("output");
const pdfLinkContainer = document.getElementById("pdf-link-container");
const openLink = document.getElementById("open-pdf");

// Show toast notification (using Flowbite Toast style)
function showToast(message, type = "info") {
  const existing = document.querySelector(".toast");
  if (existing) existing.remove();

  const toast = document.createElement("div");
  toast.className = `toast fixed bottom-6 right-6 max-w-xs w-full bg-white border rounded-lg shadow-lg p-4 flex items-center space-x-3
    ${type === "success" ? "border-green-400" : ""}
    ${type === "error" ? "border-red-400" : ""}
    ${type === "info" ? "border-blue-400" : ""}`;

  toast.innerHTML = `
    <svg class="w-6 h-6 ${
      type === "success"
        ? "text-green-500"
        : type === "error"
        ? "text-red-500"
        : "text-blue-500"
    }" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24" >
      <path stroke-linecap="round" stroke-linejoin="round" d="${
        type === "success"
          ? "M5 13l4 4L19 7"
          : type === "error"
          ? "M6 18L18 6M6 6l12 12"
          : "M13 16h-1v-4h-1m1-4h.01"
      }"/>
    </svg>
    <span class="flex-1 text-gray-700">${message}</span>
    <button class="toast-close-btn text-gray-500 hover:text-gray-700 focus:outline-none">
      &times;
    </button>
  `;
  document.body.appendChild(toast);

  toast.querySelector(".toast-close-btn").onclick = () => toast.remove();

  setTimeout(() => toast.remove(), 5000);
}

// Update Open PDF button URL and show container
function updateOpenPdfButton(url) {
  openLink.dataset.url = url;
  pdfLinkContainer.classList.remove("hidden");
  openLink.classList.remove("hidden");
}

openLink.onclick = () => {
  const url = openLink.dataset.url;
  if (url) window.open(url, "_blank");
};

form.onsubmit = async (e) => {
  e.preventDefault();
  const formData = new FormData(form);

  showToast("Uploading PDF...", "info");
  try {
    const res = await fetch("/api/upload", {
      method: "POST",
      body: formData,
    });
    if (!res.ok) throw new Error("Upload failed");
    const data = await res.json();

    // Show preview only if available, else clear text
    output.textContent = data.text_preview || "";

    updateOpenPdfButton(data.pdf_url);

    showToast("Upload successful!", "success");
  } catch (err) {
    showToast(`Error: ${err.message}`, "error");
  }
};

async function askQuery() {
  const query = document.getElementById("userQuery").value.trim();
  if (!query) {
    showToast("Please enter a question to ask.", "error");
    return;
  }

  showToast("Fetching answer...", "info");
  try {
    const res = await fetch("/api/query", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query }),
    });
    if (!res.ok) throw new Error("Failed to fetch answer");
    const data = await res.json();

    document.getElementById("answerOutput").textContent =
      `Answer: ${data.answer}\n\nSources: ${data.sources.join(", ")}`;

    const list = document.getElementById("citationsList");
    list.innerHTML = "";
    data.citations.forEach((c) => {
      const li = document.createElement("li");
      li.textContent = `[${c.score.toFixed(3)}] ${c.text.slice(0, 150)}... (source: ${c.source})`;
      list.appendChild(li);
    });

    showToast("Answer received!", "success");
  } catch (err) {
    showToast(`Error: ${err.message}`, "error");
  }
}

async function searchArxiv() {
  const query = document.getElementById("arxivInput").value.trim();
  if (!query) {
    showToast("Please enter a search term.", "error");
    return;
  }

  showToast("Searching arXiv...", "info");
  try {
    const res = await fetch(`/api/arxiv?q=${encodeURIComponent(query)}`);
    if (!res.ok) throw new Error("Failed to fetch arXiv results");
    const data = await res.json();

    const list = document.getElementById("arxivResults");
    list.innerHTML = "";

    if (data.results.length === 0) {
      list.innerHTML = "<li>No results found.</li>";
      showToast("No results found.", "info");
      return;
    }

    data.results.forEach((paper) => {
      const li = document.createElement("li");
      li.className = "mb-4 p-4 border rounded-md bg-white shadow-sm";
      li.innerHTML = `
        <h3 class="font-semibold text-lg text-gray-800">${paper.title}</h3>
        <p class="text-gray-600 mt-1">${paper.summary}</p>
        <button
          class="mt-2 bg-blue-600 text-white px-3 py-1 rounded hover:bg-blue-700 transition"
          onclick="addArxivPaper('${paper.pdf_url}')"
        >Import</button>
      `;
      list.appendChild(li);
    });

    showToast("arXiv results loaded.", "success");
  } catch (err) {
    showToast(`Error: ${err.message}`, "error");
  }
}

async function addArxivPaper(pdfUrl) {
  showToast("Importing paper...", "info");
  try {
    const res = await fetch("/api/arxiv/download", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ url: pdfUrl }),
    });
    if (!res.ok) throw new Error("Failed to import paper");
    const data = await res.json();

    alert(`✅ Imported: ${data.filename}\nChunks: ${data.chunks}`);

    updateOpenPdfButton(data.pdf_url);

    showToast("Paper imported successfully!", "success");
  } catch (err) {
    showToast(`Error: ${err.message}`, "error");
  }
}

// Add Enter key listeners for inputs
document.getElementById("arxivInput").addEventListener("keydown", (e) => {
  if (e.key === "Enter") {
    e.preventDefault();
    searchArxiv();
  }
});

document.getElementById("userQuery").addEventListener("keydown", (e) => {
  if (e.key === "Enter") {
    e.preventDefault();
    askQuery();
  }
});
