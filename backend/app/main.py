import os
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.config import settings
from app.database.db import init_db
from app.routes import profile, diagnostic, test, evaluation, feedback

logging.basicConfig(level=logging.INFO, format="%(levelname)s | %(name)s | %(message)s")
logger = logging.getLogger(__name__)

app = FastAPI(
    title="BoardAI – CBSE Mock Test Platform",
    description="AI-powered mock test generation and evaluation for CBSE Class 10 & 12 students",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static directory for downloaded PDFs
os.makedirs(settings.PDF_OUTPUT_DIR, exist_ok=True)
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
os.makedirs(settings.CHROMA_PERSIST_DIR, exist_ok=True)
app.mount("/pdfs", StaticFiles(directory=settings.PDF_OUTPUT_DIR), name="pdfs")

# Register API routes
API_PREFIX = "/api/v1"
app.include_router(profile.router, prefix=API_PREFIX)
app.include_router(diagnostic.router, prefix=API_PREFIX)
app.include_router(test.router, prefix=API_PREFIX)
app.include_router(evaluation.router, prefix=API_PREFIX)
app.include_router(feedback.router, prefix=API_PREFIX)


@app.on_event("startup")
async def startup():
    logger.info("Initialising database tables...")
    init_db()
    _seed_knowledge_base()
    logger.info("BoardAI backend ready.")


def _seed_knowledge_base():
    """Auto-seed the RAG knowledge base if empty (handles ephemeral disk on Render)."""
    try:
        from app.services import rag_service
        from data.cbse_knowledge_base import get_all_documents
        stats = rag_service.get_collection_stats()
        if stats["total_documents"] == 0:
            logger.info("Knowledge base empty — seeding CBSE content...")
            docs, metas, ids = get_all_documents()
            rag_service.add_documents(docs, metas, ids)
            logger.info(f"Seeded {len(docs)} documents into knowledge base.")
        else:
            logger.info(f"Knowledge base ready ({stats['total_documents']} documents).")
    except Exception as e:
        logger.warning(f"Knowledge base seed skipped: {e}")


@app.get("/health")
def health_check():
    return {"status": "ok", "service": "boardai-backend"}


@app.get("/")
def root():
    return {
        "message": "BoardAI API",
        "docs": "/docs",
        "version": "1.0.0",
    }
