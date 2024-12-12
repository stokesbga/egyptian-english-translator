import os
from fastapi import FastAPI
import models.audio2text as audio2text


app = FastAPI()

@app.get("/")
async def health_check():
    return {"health_check": "OK"}

@app.get("/translate")
async def translate():
    demo_path = os.path.abspath('app/demo.wav')
    en_translation = audio2text.process(demo_path)
    return {"arabic": 'stub', "english": en_translation }d