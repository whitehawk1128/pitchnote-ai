import requests
import os
from app.config import ELEVENLABS_API_KEY, VOICE_ID

def generate_voice_note(text):
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
    headers = {
        "xi-api-key": ELEVENLABS_API_KEY,
        "Content-Type": "application/json"
    }
    data = {
        "text": text,
        "model_id": "eleven_monolingual_v1"
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        folder_path = "app/static/voicenotes"
        os.makedirs(folder_path, exist_ok=True)  # <--- Create folder if not exist

        filename = os.path.join(folder_path, f"voice_{hash(text)}.mp3")
        with open(filename, "wb") as f:
            f.write(response.content)
        return filename
    else:
        raise Exception(f"TTS failed: {response.text}")
