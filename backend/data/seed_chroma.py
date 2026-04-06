#!/usr/bin/env python3
"""
Seed ChromaDB with CBSE question bank data.
Run from the backend/ directory:
    python data/seed_chroma.py
"""
import sys
import os

# Ensure we can import app modules
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from dotenv import load_dotenv
load_dotenv()

from app.services import rag_service
from data.cbse_knowledge_base import get_all_documents


def main():
    docs, metas, ids = get_all_documents()
    print(f"Seeding ChromaDB with {len(docs)} CBSE question bank entries...")
    rag_service.add_documents(docs, metas, ids)
    stats = rag_service.get_collection_stats()
    print(f"Done! Collection now has {stats['total_documents']} documents.")
    print("You can now generate tests with RAG context from the CBSE knowledge base.")


if __name__ == "__main__":
    main()
