"""Content retrieval and history endpoints."""

import json

from fastapi import APIRouter, Depends
from sqlalchemy import desc
from sqlalchemy.orm import Session

from backend.database.session import get_db
from backend.models.entities import GeneratedContent, Upload, User
from backend.models.schemas import ContentListResponse, HistoryEntryResponse
from backend.utils.deps import get_current_user

router = APIRouter(tags=["content"])


def _list_for_type(content_type: str, user: User, db: Session) -> ContentListResponse:
    """Fetch generated items for a specific revision asset type."""
    rows = (
        db.query(GeneratedContent, Upload)
        .join(Upload, Upload.id == GeneratedContent.upload_id)
        .filter(Upload.user_id == user.id, GeneratedContent.content_type == content_type)
        .order_by(desc(GeneratedContent.created_at))
        .all()
    )
    items = [
        {
            "id": row.GeneratedContent.id,
            "upload_id": row.Upload.id,
            "upload_filename": row.Upload.filename,
            "created_at": row.GeneratedContent.created_at.isoformat(),
            "content": json.loads(row.GeneratedContent.payload),
        }
        for row in rows
    ]
    return ContentListResponse(items=items)


@router.get("/summary", response_model=ContentListResponse)
async def summary(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> ContentListResponse:
    """Get generated summaries."""
    return _list_for_type("summary", current_user, db)


@router.get("/mcqs", response_model=ContentListResponse)
async def mcqs(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> ContentListResponse:
    """Get generated MCQs."""
    return _list_for_type("mcqs", current_user, db)


@router.get("/flashcards", response_model=ContentListResponse)
async def flashcards(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> ContentListResponse:
    """Get generated flashcards."""
    return _list_for_type("flashcards", current_user, db)


@router.get("/important", response_model=ContentListResponse)
async def important(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> ContentListResponse:
    """Get generated important questions."""
    return _list_for_type("important", current_user, db)


@router.get("/revision", response_model=ContentListResponse)
async def revision(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> ContentListResponse:
    """Get generated 10-minute revision guides."""
    return _list_for_type("revision", current_user, db)


@router.get("/cheatsheet", response_model=ContentListResponse)
async def cheatsheet(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> ContentListResponse:
    """Get generated cheat sheets."""
    return _list_for_type("cheatsheet", current_user, db)


@router.get("/history", response_model=list[HistoryEntryResponse])
async def history(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> list[HistoryEntryResponse]:
    """Return user generation history."""
    rows = (
        db.query(GeneratedContent, Upload)
        .join(Upload, Upload.id == GeneratedContent.upload_id)
        .filter(Upload.user_id == current_user.id)
        .order_by(desc(GeneratedContent.created_at))
        .all()
    )
    return [
        HistoryEntryResponse(
            id=row.GeneratedContent.id,
            upload_id=row.Upload.id,
            upload_filename=row.Upload.filename,
            content_type=row.GeneratedContent.content_type,
            created_at=row.GeneratedContent.created_at,
        )
        for row in rows
    ]


@router.delete("/history")
async def delete_history(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> dict:
    """Delete all generated history for current user."""
    upload_ids = [upload.id for upload in db.query(Upload).filter(Upload.user_id == current_user.id).all()]
    if upload_ids:
        db.query(GeneratedContent).filter(GeneratedContent.upload_id.in_(upload_ids)).delete(synchronize_session=False)
        db.commit()
    return {"status": "ok"}
