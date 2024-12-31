from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM, WhisperForConditionalGeneration, WhisperProcessor, WhisperTokenizer
import torch

import sys
from os import path
from pathlib import Path
import os

torch.backends.nnpack.enabled = False

os.environ["CUDA_VISIBLE_DEVICES"]=""
device = torch.device('cpu')
# torch.device("cuda" if torch.cuda.is_available() else "cpu")
print("Cuda availability: ", torch.cuda.is_available())

ARTIFACTS_DIR = Path('artifacts').resolve()


# Pipes
recognition_pipe = pipeline(model="alexstokes/whisper-small-eg2",
    torch_dtype=torch.bfloat16,
    device_map="auto")
translation_pipe = pipeline(task="translation",
                      model="facebook/nllb-200-3.3B",
                      torch_dtype=torch.bfloat16) 
# recognition_pipe = pipeline('automatic-speech-recognition', ARTIFACTS_DIR.joinpath('recognition'))
# translation_pipe = pipeline('translation', ARTIFACTS_DIR.joinpath('translate'))


def transcribe(audio_path: Path):
    audio_path = str(audio_path)
    text = recognition_pipe(audio_path)["text"]
    return text

def translate(eg_text:str):
    en_text = translation_pipe(eg_text, 
               do_sample=True, 
               temperature=0.7, 
               top_p=0.5,
               src_lang="arz_Arab",
               tgt_lang="eng_Latn",
               max_length=512)
    return en_text


def process(audio_path):
    eg_transcriptions = transcribe(audio_path)
    en_text = translate(eg_transcriptions)
    print("Translation:", en_text)
    return eg_transcriptions, en_text

if __name__=="__main__":
    if len(sys.argv) > 0:
        process(sys.argv[1])
    else:
        print("Please provide path to audio to transcribe and translate.")