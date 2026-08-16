"""AI generation endpoint."""

import json

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.database.session import get_db
from backend.models.entities import GeneratedContent, Upload, User
from backend.models.schemas import GenerateRequest, GeneratedResultResponse
from backend.services.revision_service import generate_all_outputs
from backend.utils.deps import get_current_user

router = APIRouter(tags=["generate"])


@router.post("/generate", response_model=GeneratedResultResponse)
async def generate_revision(
    payload: GenerateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> GeneratedResultResponse:
    """Generate and persist all revision outputs for a selected upload."""
    upload = db.query(Upload).filter(Upload.id == payload.upload_id, Upload.user_id == current_user.id).first()
    if not upload:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Upload not found")

    outputs = generate_all_outputs(str(upload.extracted_text))

    db.query(GeneratedContent).filter(GeneratedContent.upload_id == upload.id).delete()
    for content_type, data in outputs.items():
        db.add(GeneratedContent(upload_id=int(upload.id), content_type=content_type, payload=json.dumps(data)))
    db.commit()

    return GeneratedResultResponse(upload_id=int(upload.id), outputs=outputs)
