# VoiceAI MVP - Milestone 1

## Setup
1. `pip install -r requirements.txt`
2. Add your `.env` file
3. `uvicorn app.main:app --reload`

## Usage
POST to `/api/tts/generate` with:
```json
{
  "template": "Hi {{first_name}}, welcome to {{company}}!",
  "variables": {
    "first_name": "Alice",
    "company": "OpenAI"
  }
}
