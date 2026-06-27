"""File upload and ingestion endpoints."""

import os
import uuid
from pathlib import Path

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from backend.database.session import get_db
from backend.models.entities import Upload, User
from backend.models.schemas import UploadResponse
from backend.services.text_extraction_service import extract_text_for_file
from backend.utils.deps import get_current_user
from backend.utils.text_processing import clean_text

router = APIRouter(tags=["upload"])

ALLOWED_EXTENSIONS = {".pdf", ".docx", ".txt", ".ppt", ".pptx", ".png", ".jpg", ".jpeg"}
MAX_SIZE_BYTES = 100 * 1024 * 1024
UPLOAD_DIR = Path("backend/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


@router.post("/upload", response_model=UploadResponse)
async def upload_material(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> UploadResponse:
    """Validate uploaded file, extract text, and save upload metadata."""
    extension = Path(file.filename).suffix.lower()
    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unsupported file type")

    content = await file.read()
    if len(content) > MAX_SIZE_BYTES:
        raise HTTPException(status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE, detail="File exceeds 100MB limit")

    safe_name = f"{uuid.uuid4().hex}{extension}"
    destination = UPLOAD_DIR / safe_name
    destination.write_bytes(content)

    try:
        extracted_text = extract_text_for_file(str(destination), file.content_type or "application/octet-stream")
    except Exception as error:
        if destination.exists():
            os.remove(destination)
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=f"Extraction failed: {error}") from error

    normalized = clean_text(extracted_text)
    if len(normalized) < 30:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Extracted text is too short for AI processing")

    upload = Upload(
        user_id=current_user.id,
        filename=file.filename,
        content_type=file.content_type or "application/octet-stream",
        saved_path=str(destination),
        extracted_text=normalized,
    )
    db.add(upload)
    db.commit()
    db.refresh(upload)
    return UploadResponse(upload_id=upload.id, filename=upload.filename, extracted_characters=len(normalized))
