from transformers import AwqConfig, pipeline, AutoTokenizer, AutoModelForCausalLM, WhisperForConditionalGeneration, WhisperProcessor, WhisperTokenizer
import torch

quantization_config = AwqConfig(
    bits=8,
    fuse_max_seq_len=512,
    do_fuse=True,
)


def refresh_artifacts():

    # Pipes
    recognition_pipe = pipeline(model="alexstokes/whisper-small-eg2",
                                torch_dtype=torch.bfloat16,
                                device_map="cpu")
    translate_pipe = pipeline(task="translation",
                      model="facebook/nllb-200-3.3B",
                      torch_dtype=torch.bfloat16, device_map="cpu")
                            # model_kwargs={"quantization_config": quantization_config})
                            # model_kwargs={"llm_int8_enable_fp32_cpu_offload":True, "load_in_8bit": True})

    recognition_pipe.save_pretrained('artifacts/recognition', 
                                     low_cpu_mem_usage=True, 
                                     safe_serialization=True,
                                     max_shard_size="100MB", 
                                     quantization_config=quantization_config)
    translate_pipe.save_pretrained('artifacts/translate', 
                                   low_cpu_mem_usage=True, 
                                   safe_serialization=True, 
                                   max_shard_size="300MB",
                                   quantization_config=quantization_config)

def refresh_checkpoints():
    recog_tokenizer = AutoTokenizer.from_pretrained("alexstokes/whisper-small-eg2", language="Arabic")
    recog_model = AutoModelForCausalLM.from_pretrained("alexstokes/whisper-small-eg2", torch_dtype=torch.float16)
    
    translate_tokenizer = AutoTokenizer.from_pretrained("ahmedsamirio/Egyptian-Arabic-Translator-Llama-3-8B")
    translate_model = AutoModelForCausalLM.from_pretrained("ahmedsamirio/Egyptian-Arabic-Translator-Llama-3-8B", torch_dtype=torch.float16)
    
    
    recog_tokenizer.save_pretrained(safe_serialization=True, save_directory="shards/recog/tokenizer")
    recog_model.save_pretrained(safe_serialization=True, save_directory="shards/recog/model")
    translate_tokenizer.save_pretrained(safe_serialization=True, save_directory="shards/translate/tokenizer")
    translate_model.save_pretrained(safe_serialization=True, save_directory="shards/translate/model")


if __name__=="__main__":
    refresh_artifacts()