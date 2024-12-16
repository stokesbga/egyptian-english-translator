import os
from fastapi import FastAPI, File, UploadFile, HTTPException
import app.models.audio2text as audio2text
from pydantic import BaseModel
import shutil
from typing import Optional

UPLOADS_DIR = os.path.abspath('app/uploads')

class TextPayload(BaseModel):
    route: str | None = "None"
    arabic_text: str = ""

app = FastAPI()

def health_check():
    return {"health_check": "OK"}

def translate_demo():
    demo_path = os.path.abspath('app/demo.wav')
    eg_transcriptions, en_translation = audio2text.process(demo_path)
    return {"arabic": eg_transcriptions, "english": en_translation }

def translate_text(arabic_text: str):
    translation = audio2text.translate(arabic_text)
    return {"arabic": arabic_text, "english": translation }

def translate_audio_upload(audio_file: UploadFile = File(...)):
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


# API ROUTES OUTSIDE OF INVOKE
@app.get("/")
def health_check_api():
    return health_check()

@app.get("/translate-demo")
def translate_demo_api():
    return translate_demo()

@app.get("/translate-text")
def translate_text_api(arabic_text: str):
    return translate_text(arabic_text)

@app.post("/translate-audio")
def translate_audio_upload_api(audio_file: UploadFile = File(...)):
    return translate_audio_upload(audio_file)

# AWS INVOCATION ROUTE 
@app.post('/invocations')
def invoke(audio_file: UploadFile | None = None, route: str = "None", arabic_text: str = ""):
    if audio_file is not None:
        return translate_audio_upload(audio_file)
    elif route == 'translate_text' and len(arabic_text) > 0:
        return translate_text(arabic_text)
    elif route == 'translate_demo':  
        return translate_demo()
    else:
      return health_check()