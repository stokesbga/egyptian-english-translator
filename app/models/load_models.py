from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM, WhisperForConditionalGeneration, WhisperProcessor, WhisperTokenizer
import torch

import sys
import os

# Pipes
recognition_pipe = pipeline(model="alexstokes/whisper-small-eg2",
    torch_dtype=torch.bfloat16,
    device_map="auto")
translate_pipe = pipeline(model="ahmedsamirio/Egyptian-Arabic-Translator-Llama-3-8B")
