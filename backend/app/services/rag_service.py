"""
RAG service using in-memory TF-IDF similarity search.
Replaces ChromaDB — works on Python 3.13 with no C++ compilation.
The knowledge base is small (~35 docs) so in-memory is perfectly fine.
"""
import json
import logging
import os
from typing import List, Dict

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

logger = logging.getLogger(__name__)

# In-memory store: loaded once at first query
_documents: List[str] = []
_metadatas: List[Dict] = []
_ids: List[str] = []
_vectorizer: TfidfVectorizer | None = None
_matrix = None  # sparse TF-IDF matrix

PERSIST_PATH = "./chroma_data/knowledge_base.json"  # reuse existing dir name


def _save_to_disk():
    os.makedirs(os.path.dirname(PERSIST_PATH), exist_ok=True)
    with open(PERSIST_PATH, "w", encoding="utf-8") as f:
        json.dump({"documents": _documents, "metadatas": _metadatas, "ids": _ids}, f, indent=2)


def _load_from_disk():
    global _documents, _metadatas, _ids
    if os.path.exists(PERSIST_PATH):
        with open(PERSIST_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        _documents[:] = data.get("documents", [])
        _metadatas[:] = data.get("metadatas", [])
        _ids[:] = data.get("ids", [])
        logger.info(f"Loaded {len(_documents)} docs from disk")


def _build_index():
    global _vectorizer, _matrix
    if not _documents:
        return
    _vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
    _matrix = _vectorizer.fit_transform(_documents)


def _ensure_loaded():
    if not _documents:
        _load_from_disk()
        _build_index()


def add_documents(documents: List[str], metadatas: List[Dict], ids: List[str]) -> None:
    """Add/replace documents in the in-memory store and persist to disk."""
    global _documents, _metadatas, _ids
    existing_ids = set(_ids)
    for doc, meta, doc_id in zip(documents, metadatas, ids):
        if doc_id in existing_ids:
            idx = _ids.index(doc_id)
            _documents[idx] = doc
            _metadatas[idx] = meta
        else:
            _documents.append(doc)
            _metadatas.append(meta)
            _ids.append(doc_id)
    _build_index()
    _save_to_disk()
    logger.info(f"Knowledge base now has {len(_documents)} documents")


def query_context(
    class_level: int,
    subject: str,
    topics: List[str],
    n_results: int = 8,
) -> str:
    """Retrieve relevant CBSE content using TF-IDF cosine similarity."""
    _ensure_loaded()
    if not _documents or _vectorizer is None:
        logger.warning("Knowledge base is empty. Run data/seed_chroma.py first.")
        return ""

    query = f"Class {class_level} {subject} {' '.join(topics[:4])}"
    query_vec = _vectorizer.transform([query])
    scores = cosine_similarity(query_vec, _matrix)[0]

    # Boost docs matching class_level and subject metadata
    boosted = scores.copy()
    for i, meta in enumerate(_metadatas):
        if meta.get("class_level") == class_level and meta.get("subject") == subject:
            boosted[i] *= 1.5

    top_idx = np.argsort(boosted)[::-1][:n_results]
    top_docs = [_documents[i] for i in top_idx if boosted[i] > 0]

    return "\n---\n".join(top_docs) if top_docs else ""


def get_collection_stats() -> Dict:
    _ensure_loaded()
    return {"total_documents": len(_documents), "collection_name": "in_memory_tfidf"}
