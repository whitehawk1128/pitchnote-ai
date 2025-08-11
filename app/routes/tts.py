from fastapi import APIRouter
from pydantic import BaseModel
from typing import Dict
from app.services.tts_engine import generate_voice_note
from app.utils.templating import render_template

router = APIRouter()

# ✅ Define a schema using Pydantic
class AudioRequest(BaseModel):
    template: str
    variables: Dict[str, str]

@router.post("/generate")
async def generate_audio(request: AudioRequest):
    # You can now access template and variables directly
    message = render_template(request.template, request.variables)
    file_path = generate_voice_note(message)
    return {"audio_path": file_path}
