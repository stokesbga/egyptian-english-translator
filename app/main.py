import os
from fastapi import FastAPI, File, UploadFile, HTTPException
import models.audio2text as audio2text
import shutil

UPLOADS_DIR = os.path.abspath('app/uploads')

app = FastAPI()

@app.get("/")
async def health_check():
    return {"health_check": "OK"}

@app.get("/translate-demo")
async def translate():
    demo_path = os.path.abspath('app/demo.wav')
    eg_transcriptions, en_translation = audio2text.process(demo_path)
    return {"arabic": eg_transcriptions, "english": en_translation }

@app.get("/translate-text")
async def translate(arabic_text: str):
    translation = audio2text.translate(arabic_text)
    return {"arabic": arabic_text, "english": translation }

@app.post("/translate-audio")
def upload(audio_file: UploadFile = File(...)):
    write_file_path = UPLOADS_DIR+'/'+audio_file.filename.replace(' ', '-')
    try:
        with open(write_file_path, 'wb+') as f:
            shutil.copyfileobj(audio_file.file, f)
    except Exception:
        raise HTTPException(status_code=500, detail='Something went wrong uploading the file')
    finally:
        audio_file.file.close()
    
    eg_transcriptions, en_translation = audio2text.process(write_file_path)
    os.remove(write_file_path)
    return {"arabic": eg_transcriptions, "english": en_translation }