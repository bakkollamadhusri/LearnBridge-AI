from fastapi import APIRouter, Query, HTTPException
from ..services.diagram_service import DiagramService
from ..services.video_service import VideoService
from ..config import settings

router = APIRouter(prefix="/media", tags=["Educational Media & Diagrams"])

@router.get("/diagram")
async def get_diagram(topic: str = Query(...)):
    """Retrieves an interactive educational vector SVG diagram for the given topic."""
    diag = DiagramService.get_diagram_for_topic(topic)
    if not diag:
        raise HTTPException(status_code=404, detail="No diagram available for this topic.")
    return diag

@router.get("/videos")
async def get_videos(topic: str = Query(...), language: str = Query("English")):
    """Retrieves authentic educational video tutorials with language matching."""
    videos = VideoService.get_videos_for_topic(topic, preferred_language=language)
    return {"topic": topic, "language": language, "videos": videos}

@router.get("/languages")
async def get_supported_languages():
    """Returns list of supported regional languages in LearnBridge AI."""
    return {
        "supported_languages": settings.SUPPORTED_LANGUAGES,
        "default": "English",
        "regional_highlights": ["Telugu", "Hindi", "Tamil", "Kannada", "Malayalam", "Marathi", "Bengali"]
    }
