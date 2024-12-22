import json
import logging
import torch
from pathlib import Path
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM, WhisperForConditionalGeneration, WhisperProcessor, WhisperTokenizer
import app.models.audio2text as audio2text
import shutil
import os

torch.device('cuda' if torch.cuda.is_available else 'cpu')

UPLOADS_DIR = os.path.abspath('app/uploads')
logger = logging.getLogger(__name__)


def health_check():
    return {"health_check": "OK"}

def translate_demo():
    demo_path = os.path.abspath('app/demo.wav')
    eg_transcriptions, en_translation = audio2text.process(demo_path)
    return {"arabic": eg_transcriptions, "english": en_translation }

def translate_text(arabic_text: str):
    translation = audio2text.translate(arabic_text)
    return {"arabic": arabic_text, "english": translation }

def translate_audio_upload(audio_file):
    write_file_path = UPLOADS_DIR+'/'+audio_file.filename.replace(' ', '-')
    try:
        with open(write_file_path, 'wb+') as f:
            shutil.copyfileobj(audio_file.file, f)
    except Exception:
        raise Exception(status_code=500, detail='Something went wrong uploading the file')
    finally:
        audio_file.file.close()
    
    eg_transcriptions, en_translation = audio2text.process(write_file_path)
    os.remove(write_file_path)
    return {"arabic": eg_transcriptions, "english": en_translation }




class ModelHandler:
    def __init__(self):
        self.initialized = False
        self.mx_model = None
        self.shapes = None

    def initialize(self, ctx):
        """ In this initialize function, the model is loaded and
           initialized here.
        Args:
            ctx (context): It is a JSON Object containing information
            pertaining to the model artifacts parameters.
        """
        self.manifest = ctx.manifest
        properties = ctx.system_properties
        artifact_path = properties.get("model_dir")
        self.batch_size = properties.get("batch_size")

        # Load pipelines and artifacts
        self.recognition_pipe = pipeline(model="alexstokes/whisper-small-eg2") 
        self.translate_pipe = pipeline(model="ahmedsamirio/Egyptian-Arabic-Translator-Llama-3-8B")
        self.initialized = True

    def preprocess(self, data):
        """
        Preprocess function to convert the request input to the desired format.
        """
        return data.model_dump_json()

    def inference(self, data):
        """
        The Inference Function makes a prediction call on the given input request.
        """
        logger.debug('payload: ', data)
        if data.get('audio_file') is not None:
            return translate_audio_upload(data['audio_file'])
        
        route, arabic_text = data.get('route'), data.get('arabic_text')
        if route == 'translate_demo':  
            return translate_demo()
        
        if route == 'translate_text' and len(arabic_text) > 0:
            return translate_text(arabic_text)
        
        return health_check()

    def postprocess(self, inference_output):
        """
        Return predict result in the desired format
        """
        return inference_output
        

    def handle(self, data, context):
        """
        Call preprocess, inference and post-process functions
        :param data: input data
        :param context: mms context
        """

        model_input = self.preprocess(data)
        model_out = self.inference(model_input)
        return self.postprocess(model_out)

_service = ModelHandler()


def handle(data, context):
    if not _service.initialized:
        _service.initialize(context)

    if data is None:
        return None
    logger.debug('handler called with data: ', data)
    return _service.handle(data, context)