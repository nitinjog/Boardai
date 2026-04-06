"""
File upload handling for scanned answer sheets.
"""
import os
import uuid
import logging
from typing import Tuple
from fastapi import UploadFile, HTTPException
from app.config import settings

logger = logging.getLogger(__name__)

ALLOWED_TYPES = {
    "image/jpeg": ".jpg",
    "image/png": ".png",
    "image/webp": ".webp",
    "application/pdf": ".pdf",
}


async def save_uploaded_file(file: UploadFile, subfolder: str = "answers") -> Tuple[str, str]:
    """
    Validate and save an uploaded file.
    Returns (file_path, mime_type).
    """
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type '{file.content_type}'. Allowed: {list(ALLOWED_TYPES.keys())}",
        )

    content = await file.read()
    size_mb = len(content) / (1024 * 1024)
    if size_mb > settings.MAX_UPLOAD_SIZE_MB:
        raise HTTPException(
            status_code=413,
            detail=f"File size {size_mb:.1f} MB exceeds limit of {settings.MAX_UPLOAD_SIZE_MB} MB",
        )

    ext = ALLOWED_TYPES[file.content_type]
    filename = f"{uuid.uuid4()}{ext}"
    save_dir = os.path.join(settings.UPLOAD_DIR, subfolder)
    os.makedirs(save_dir, exist_ok=True)
    filepath = os.path.join(save_dir, filename)

    with open(filepath, "wb") as f:
        f.write(content)

    logger.info(f"Saved upload: {filepath} ({size_mb:.2f} MB)")
    return filepath, file.content_type


def read_file_bytes(filepath: str) -> bytes:
    with open(filepath, "rb") as f:
        return f.read()
