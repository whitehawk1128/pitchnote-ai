from fastapi import FastAPI
from app.routes import tts
from app.routes import linkedin

app = FastAPI()
app.include_router(tts.router, prefix="/api/tts")
app.include_router(linkedin.router, prefix="/api/linkedin")

@app.get("/")
async def root():
    return {"message": "Hello, Render!"}