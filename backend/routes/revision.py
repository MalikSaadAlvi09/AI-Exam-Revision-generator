import mimetypes
import os
from pathlib import Path

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from backend.database.session import get_db
from backend.models import GeneratedContent, Upload, User
from backend.schemas import GenerateRequest, GenerateResponse, HistoryItem, UploadResponse
from backend.services import GenerationService, TextExtractionService
from backend.utils.dependencies import get_current_user

router = APIRouter(tags=["revision"])

UPLOAD_DIR = Path(os.getenv("UPLOAD_DIR", "backend/uploads"))
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

ALLOWED_EXTENSIONS = {".pdf", ".docx", ".txt", ".ppt", ".pptx", ".png", ".jpg", ".jpeg"}
MAX_FILE_SIZE = 100 * 1024 * 1024


@router.post("/upload", response_model=UploadResponse)
async def upload_file(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    extension = Path(file.filename).suffix.lower()
    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Unsupported file type")

    file_bytes = await file.read()
    if len(file_bytes) > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="File exceeds 100MB limit")

    save_path = UPLOAD_DIR / f"{current_user.id}_{file.filename}"
    save_path.write_bytes(file_bytes)

    try:
        extracted_text = TextExtractionService.extract_text(save_path)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Text extraction failed: {exc}") from exc

    if not extracted_text.strip():
        raise HTTPException(status_code=400, detail="No readable text found in the uploaded file")

    upload = Upload(
        user_id=current_user.id,
        filename=file.filename,
        stored_path=str(save_path),
        mime_type=file.content_type or mimetypes.guess_type(file.filename)[0] or "application/octet-stream",
        extracted_text=extracted_text,
    )
    db.add(upload)
    db.commit()
    db.refresh(upload)

    return UploadResponse(upload_id=upload.id, filename=upload.filename, mime_type=upload.mime_type)


@router.post("/generate", response_model=GenerateResponse)
def generate_content(
    payload: GenerateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    upload = None
    source_text = payload.raw_text

    if payload.upload_id:
        upload = db.query(Upload).filter(Upload.id == payload.upload_id, Upload.user_id == current_user.id).first()
        if not upload:
            raise HTTPException(status_code=404, detail="Upload not found")
        source_text = upload.extracted_text

    if not source_text or len(source_text.strip()) < 10:
        raise HTTPException(status_code=400, detail="Provide upload_id or meaningful raw_text")

    if not upload:
        upload = Upload(
            user_id=current_user.id,
            filename="pasted_text.txt",
            stored_path="inline",
            mime_type="text/plain",
            extracted_text=source_text,
        )
        db.add(upload)
        db.commit()
        db.refresh(upload)

    outputs = GenerationService().generate_all(source_text)

    db.query(GeneratedContent).filter(GeneratedContent.upload_id == upload.id).delete()
    for content_type, generated_text in outputs.items():
        db.add(GeneratedContent(upload_id=upload.id, content_type=content_type, payload=generated_text))
    db.commit()

    return GenerateResponse(upload_id=upload.id, outputs=outputs)


@router.get("/history", response_model=list[HistoryItem])
def get_history(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    uploads = db.query(Upload).filter(Upload.user_id == current_user.id).order_by(Upload.created_at.desc()).all()
    result = []
    for item in uploads:
        generated_types = [g.content_type for g in item.generated_items]
        result.append(
            HistoryItem(
                upload_id=item.id,
                filename=item.filename,
                created_at=item.created_at,
                generated_types=generated_types,
            )
        )
    return result


@router.delete("/history")
def delete_history(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    uploads = db.query(Upload).filter(Upload.user_id == current_user.id).all()
    for upload in uploads:
        if upload.stored_path != "inline":
            path = Path(upload.stored_path)
            if path.exists():
                path.unlink()
        db.delete(upload)
    db.commit()
    return {"message": "History deleted"}


def _get_generated_item(content_type: str, upload_id: int, db: Session, user_id: int):
    item = (
        db.query(GeneratedContent)
        .join(Upload, Upload.id == GeneratedContent.upload_id)
        .filter(GeneratedContent.content_type == content_type, Upload.id == upload_id, Upload.user_id == user_id)
        .first()
    )
    if not item:
        raise HTTPException(status_code=404, detail=f"No {content_type} generated for this upload")
    return {"upload_id": upload_id, "type": content_type, "content": item.payload}


@router.get("/summary")
def get_summary(upload_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return _get_generated_item("summary", upload_id, db, current_user.id)


@router.get("/mcqs")
def get_mcqs(upload_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return _get_generated_item("mcqs", upload_id, db, current_user.id)


@router.get("/flashcards")
def get_flashcards(upload_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return _get_generated_item("flashcards", upload_id, db, current_user.id)


@router.get("/important")
def get_important(upload_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return _get_generated_item("important", upload_id, db, current_user.id)


@router.get("/revision")
def get_revision(upload_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return _get_generated_item("revision", upload_id, db, current_user.id)


@router.get("/cheatsheet")
def get_cheatsheet(upload_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return _get_generated_item("cheatsheet", upload_id, db, current_user.id)
