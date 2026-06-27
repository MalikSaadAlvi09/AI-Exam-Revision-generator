"""Profile endpoints."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.database.session import get_db
from backend.models.entities import User
from backend.models.schemas import UserProfileResponse, UserProfileUpdateRequest
from backend.utils.deps import get_current_user

router = APIRouter(tags=["profile"])


@router.get("/profile", response_model=UserProfileResponse)
async def get_profile(current_user: User = Depends(get_current_user)) -> UserProfileResponse:
    """Return profile details for the authenticated user."""
    return UserProfileResponse(
        id=current_user.id,
        email=current_user.email,
        full_name=current_user.full_name,
        dark_mode=current_user.dark_mode,
        created_at=current_user.created_at,
    )


@router.put("/profile", response_model=UserProfileResponse)
async def update_profile(
    payload: UserProfileUpdateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> UserProfileResponse:
    """Update editable user profile values."""
    current_user.full_name = payload.full_name
    current_user.dark_mode = payload.dark_mode
    db.add(current_user)
    db.commit()
    db.refresh(current_user)
    return UserProfileResponse(
        id=current_user.id,
        email=current_user.email,
        full_name=current_user.full_name,
        dark_mode=current_user.dark_mode,
        created_at=current_user.created_at,
    )
