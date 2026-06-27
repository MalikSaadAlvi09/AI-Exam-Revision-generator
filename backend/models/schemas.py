"""Pydantic request/response schemas."""

from datetime import datetime
from typing import Any, Dict, List
from pydantic import BaseModel, EmailStr, Field


class RegisterRequest(BaseModel):
    """Input schema for creating a new account."""

    email: EmailStr
    full_name: str = Field(min_length=2, max_length=255)
    password: str = Field(min_length=8, max_length=64)


class LoginRequest(BaseModel):
    """Input schema for authentication."""

    email: EmailStr
    password: str = Field(min_length=8, max_length=64)


class TokenResponse(BaseModel):
    """JWT bearer token response."""

    access_token: str
    token_type: str = "bearer"


class UserProfileResponse(BaseModel):
    """User profile output schema."""

    id: int
    email: EmailStr
    full_name: str
    dark_mode: bool
    created_at: datetime


class UserProfileUpdateRequest(BaseModel):
    """Profile update input schema."""

    full_name: str = Field(min_length=2, max_length=255)
    dark_mode: bool


class UploadResponse(BaseModel):
    """Upload response schema."""

    upload_id: int
    filename: str
    extracted_characters: int


class GenerateRequest(BaseModel):
    """Generate pipeline input schema."""

    upload_id: int


class GeneratedResultResponse(BaseModel):
    """Combined generation output."""

    upload_id: int
    outputs: Dict[str, Any]


class HistoryEntryResponse(BaseModel):
    """Revision history entry schema."""

    id: int
    upload_id: int
    upload_filename: str
    content_type: str
    created_at: datetime


class ContentListResponse(BaseModel):
    """Output list schema for generated assets."""

    items: List[Dict[str, Any]]
