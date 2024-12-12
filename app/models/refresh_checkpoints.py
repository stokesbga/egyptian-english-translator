from transformers import AutoTokenizer, AutoModelForCausalLM, WhisperForConditionalGeneration, WhisperProcessor, WhisperTokenizer
import torch



def refresh_checkpoints():
    recog_tokenizer = AutoTokenizer.from_pretrained("alexstokes/whisper-small-eg2", language="Arabic")
    recog_model = AutoModelForCausalLM.from_pretrained("alexstokes/whisper-small-eg2", torch_dtype=torch.float16)
    # recog_model.generation_config.task = 'transcribe'
    
    translate_tokenizer = AutoTokenizer.from_pretrained("ahmedsamirio/Egyptian-Arabic-Translator-Llama-3-8B")
    translate_model = AutoModelForCausalLM.from_pretrained("ahmedsamirio/Egyptian-Arabic-Translator-Llama-3-8B", torch_dtype=torch.float16)
    
    
    recog_tokenizer.save_pretrained(safe_serialization=True, save_directory="shards/recog/tokenizer")
    recog_model.save_pretrained(safe_serialization=True, save_directory="shards/recog/model")
    translate_tokenizer.save_pretrained(safe_serialization=True, save_directory="shards/translate/tokenizer")
    translate_model.save_pretrained(safe_serialization=True, save_directory="shards/translate/model")


if __name__=="__main__":
    refresh_checkpoints()