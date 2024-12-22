import os
from fastapi import File, UploadFile, HTTPException
import models.audio2text as audio2text
import shutil
from pathlib import Path


UPLOADS_DIR = Path('uploads').resolve()
DEMO_WAV = Path('demo.wav').resolve()


def health_check(_ = None):
    return {"health_check": "OK"}

def translate_text(eg_t: str):
    translation = audio2text.translate(eg_t)
    return {"arabic": eg_t, "english": translation }

def translate_audio_demo(_ = None):
    print('DEMO WAV PATH')
    print(DEMO_WAV)
    eg_transcriptions, en_translation = audio2text.process(str(DEMO_WAV))
    return {"arabic": eg_transcriptions, "english": en_translation }

def translate_audio_upload(audio_file: UploadFile = File(...)):
    write_file_path = str(UPLOADS_DIR.joinpath(audio_file.filename.replace(' ', '-')).resolve())
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


MODEL_MAP = {
    "health_check": health_check,
    "translate_text": translate_text,
    "translate_audio_demo": translate_audio_demo,
    "translate_audio_upload": translate_audio_upload
}
