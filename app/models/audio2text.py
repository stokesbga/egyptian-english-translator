from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from numba import cuda
import torch
import sys

recog_pipe = pipeline(model="alexstokes/whisper-small-eg")

# Take recognition and pipe to Translator
tokenizer = AutoTokenizer.from_pretrained("ahmedsamirio/Egyptian-Arabic-Translator-Llama-3-8B")
model = AutoModelForCausalLM.from_pretrained("ahmedsamirio/Egyptian-Arabic-Translator-Llama-3-8B",
                                              torch_dtype=torch.float16,
                                               load_in_8bit=True)
                                                # attn_implementation="flash_attention_2")
pipe = pipeline(task='text-generation', model=model, tokenizer=tokenizer)


en_template = """<|begin_of_text|>Below is an instruction that describes a task, paired with an input that provides further context. Write a response that appropriately completes the request.

### Instruction:
Translate the following text to English.

### Input:
{message}

### Response:
"""


def transcribe(audio_path):
    text = recog_pipe(audio_path)["text"]
    return text

def translate(eg_text:str):
    en_text = pipe(en_template.format(message=eg_text), 
               max_new_tokens=512, 
               do_sample=True, 
               temperature=0.7, 
               top_p=0.5)
    return en_text


def process(audio_path):
    eg_transcriptions = transcribe(audio_path)
    en_text = translate(eg_transcriptions)
    print("Translation:", en_text)
    return en_text

if __name__=="__main__":
    if len(sys.argv) > 0:
        process(sys.argv[1])
    else:
        print("Please provide path to audio to transcribe and translate.")