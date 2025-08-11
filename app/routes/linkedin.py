from fastapi import APIRouter, UploadFile, Form, File
from app.services.linkedin_service import handle_linkedin_voice_message

router = APIRouter()

@router.post("/send-voice")
async def send_voice(
    keywords: str = Form(...),
    voice_message: UploadFile = File(...)
):
    result = await handle_linkedin_voice_message(keywords, voice_message)
    return result
