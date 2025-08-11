import httpx
from fastapi import UploadFile

UNIPILE_API_KEY = "DxRU2r5g.JMT7av53Li5WGN3R8LKDfpkKUBFlw14IX9zbddivc90="
ACCOUNT_ID = "RWyl1qXtRROvj0QM5ea5lw"
SEARCH_URL = f"https://api17.unipile.com:14787/api/v1/linkedin/search?limit=50&account_id={ACCOUNT_ID}"
SEND_URL = "https://api17.unipile.com:14787/api/v1/chats"

headers_json = {
    "X-API-KEY": UNIPILE_API_KEY,
    "accept": "application/json",
    "content-type": "application/json"
}

headers_form = {
    "X-API-KEY": UNIPILE_API_KEY,
    "accept": "application/json"
}


async def handle_linkedin_voice_message(keywords: str, voice_message: UploadFile):
    payload = {
        "api": "classic",
        "category": "people",
        "network_distance": [1],
        "keywords": keywords
    }

    # Set longer timeout (60s)
    timeout = httpx.Timeout(60.0)

    async with httpx.AsyncClient(timeout=timeout) as client:
        search_response = await client.post(SEARCH_URL, headers=headers_json, json=payload)

    people = search_response.json().get("items", [])
    attendee_ids = [person["id"] for person in people if "id" in person]

    if not attendee_ids:
        return {"status": "error", "message": "No attendees found"}
    
    results = []
    for attendee_id in attendee_ids:
        # Reset file pointer before each send
        voice_message.file.seek(0)

        data = {
            "attendees_ids": (None, attendee_id),
            "account_id": (None, ACCOUNT_ID),
            "voice_message": (voice_message.filename, voice_message.file, voice_message.content_type),
        }

        try:
            # USE TIMEOUT HERE AS WELL
            async with httpx.AsyncClient(timeout=timeout) as client:
                response = await client.post(SEND_URL, headers=headers_form, files=data)
                result = {
                    "attendee_id": attendee_id,
                    "status": response.status_code,
                    "response": response.json()
                }
        except httpx.HTTPError as e:
            result = {
                "attendee_id": attendee_id,
                "status": "error",
                "error": str(e)
            }

        results.append(result)

    return {"status": "success", "sent": results}
