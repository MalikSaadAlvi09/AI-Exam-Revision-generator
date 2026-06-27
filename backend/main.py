"""FastAPI application entrypoint."""

import os
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from backend.database.session import Base, engine
from backend.routes.auth import router as auth_router
from backend.routes.content import router as content_router
from backend.routes.generate import router as generate_router
from backend.routes.profile import router as profile_router
from backend.routes.upload import router as upload_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Exam Revision Generator", version="1.0.0")

allowed_origins = os.getenv("ALLOWED_ORIGINS", "*").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in allowed_origins],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(upload_router)
app.include_router(generate_router)
app.include_router(content_router)
app.include_router(profile_router)

frontend_dir = Path("frontend")
if frontend_dir.exists():
    app.mount("/frontend", StaticFiles(directory=str(frontend_dir), html=True), name="frontend")


@app.get("/")
async def index():
    """Serve landing page when frontend directory is present."""
    landing = frontend_dir / "index.html"
    if landing.exists():
        return FileResponse(str(landing))
    return {"status": "ok", "message": "Frontend not found"}
