"""
SmartCollegeBot - PDF Document Q&A
"""

import json
import os
import re
from datetime import datetime
from uuid import uuid4

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

DOC_FILE = os.path.join(os.path.dirname(__file__), "documents.json")


def _load_documents():
    if os.path.exists(DOC_FILE):
        with open(DOC_FILE, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []


def _save_documents(documents):
    with open(DOC_FILE, "w", encoding="utf-8") as f:
        json.dump(documents, f, indent=2)


def _extract_pdf_text(uploaded_file):
    try:
        from pypdf import PdfReader
    except ImportError:
        try:
            from PyPDF2 import PdfReader
        except ImportError as exc:
            raise RuntimeError("Install pypdf to enable PDF Q&A: pip install pypdf") from exc

    reader = PdfReader(uploaded_file)
    pages = []
    for page_num, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        text = re.sub(r"\s+", " ", text).strip()
        if text:
            pages.append({"page": page_num, "text": text})
    return pages


def _chunk_pages(pages, chunk_size=900, overlap=160):
    chunks = []
    for page in pages:
        text = page["text"]
        start = 0
        while start < len(text):
            chunk = text[start:start + chunk_size].strip()
            if chunk:
                chunks.append({"page": page["page"], "text": chunk})
            if start + chunk_size >= len(text):
                break
            start += chunk_size - overlap
    return chunks


def add_pdf_document(uploaded_file, title: str, uploaded_by: str):
    pages = _extract_pdf_text(uploaded_file)
    chunks = _chunk_pages(pages)
    if not chunks:
        return False, "No readable text found in this PDF."

    documents = _load_documents()
    document = {
        "id": str(uuid4()),
        "title": title.strip() or uploaded_file.name,
        "filename": uploaded_file.name,
        "uploaded_by": uploaded_by,
        "uploaded_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "pages": len(pages),
        "chunks": chunks,
    }
    documents.append(document)
    _save_documents(documents)
    return True, f"Uploaded {document['title']} with {len(chunks)} searchable sections."


def get_documents():
    return sorted(_load_documents(), key=lambda d: d.get("uploaded_at", ""), reverse=True)


def delete_document(document_id: str):
    documents = _load_documents()
    updated = [d for d in documents if d.get("id") != document_id]
    if len(updated) == len(documents):
        return False, "Document not found."
    _save_documents(updated)
    return True, "Document deleted."


def answer_from_documents(question: str, document_id: str | None = None, top_k: int = 3):
    documents = _load_documents()
    if document_id:
        documents = [d for d in documents if d.get("id") == document_id]
    passages = []
    for doc in documents:
        for chunk in doc.get("chunks", []):
            passages.append({
                "document": doc.get("title", "Document"),
                "page": chunk.get("page"),
                "text": chunk.get("text", ""),
            })

    if not passages:
        return None

    corpus = [question] + [p["text"] for p in passages]
    vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2), max_features=6000)
    matrix = vectorizer.fit_transform(corpus)
    scores = cosine_similarity(matrix[0:1], matrix[1:]).flatten()
    ranked = scores.argsort()[-top_k:][::-1]

    matches = []
    for idx in ranked:
        score = float(scores[idx])
        if score <= 0:
            continue
        passage = passages[idx].copy()
        passage["score"] = score
        matches.append(passage)

    if not matches:
        return None

    answer_lines = ["I found this in the uploaded documents:"]
    for match in matches:
        excerpt = match["text"]
        if len(excerpt) > 520:
            excerpt = excerpt[:520].rsplit(" ", 1)[0] + "..."
        answer_lines.append(
            f"**{match['document']}**, page {match['page']} "
            f"(match {match['score']:.0%}):\n{excerpt}"
        )
    return "\n\n".join(answer_lines)
