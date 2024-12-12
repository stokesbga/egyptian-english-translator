import os
from fastapi import FastAPI
import models.audio2text as audio2text


app = FastAPI()

@app.get("/")
async def health_check():
    return {"health_check": "OK"}

@app.post("/translate")
async def translate(audio_upload: str):
    demo_path = os.path.abspath(audio_upload)
    eg_transcriptions, en_translation = audio2text.process(demo_path)
    return {"arabic": eg_transcriptions, "english": en_translation }