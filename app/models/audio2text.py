from transformers import pipeline
import torch
import sys

torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Pipes
recognition_pipe = pipeline(task="automatic-speech-recognition", model='shards/recog/model', tokenizer='shards/recog/tokenizer')
translate_pipe = pipeline(task='text-generation', model='shards/translate/model', tokenizer='shards/translate/model')


LLAMA_EN_TEMPLATE = """<|begin_of_text|>Below is an instruction that describes a task, paired with an input that provides further context. Write a response that appropriately completes the request.

### Instruction:
Translate the following text to English.

### Input:
{message}

### Response:
"""


def transcribe(audio_path):
    text = recognition_pipe(audio_path)["text"]
    return text

def translate(eg_text:str):
    en_text = translate_pipe(LLAMA_EN_TEMPLATE.format(message=eg_text), 
               max_new_tokens=512, 
               do_sample=True, 
               temperature=0.7, 
               top_p=0.5)
    en_text = en_text[0]['generated_text'].split('### Response:\n',1)[1]
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