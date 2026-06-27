from datetime import datetime
from typing import Dict, List, Optional

from pydantic import BaseModel, EmailStr, Field


class RegisterRequest(BaseModel):
    email: EmailStr
    full_name: str = Field(min_length=2, max_length=255)
    password: str = Field(min_length=8, max_length=128)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    full_name: str
    created_at: datetime

    class Config:
        from_attributes = True


class GenerateRequest(BaseModel):
    upload_id: Optional[int] = None
    raw_text: Optional[str] = Field(default=None, min_length=10)


class GenerateResponse(BaseModel):
    upload_id: int
    outputs: Dict[str, str]


class UploadResponse(BaseModel):
    upload_id: int
    filename: str
    mime_type: str


class HistoryItem(BaseModel):
    upload_id: int
    filename: str
    created_at: datetime
    generated_types: List[str]
