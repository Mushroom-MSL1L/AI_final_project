#traing llama2 model by using LoRA

import os
import torch
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    BitsAndBytesConfig,
    HfArgumentParser,
    TrainingArguments,
    pipeline,
    logging,
)
from peft import LoraConfig, PeftModel
from trl import SFTTrainer

model = r"llama.cpp/llama-2-7b-chat.Q5_K_M.gguf"
dataset = ""
new_model = "Llama-2-7b-chat-finetune"

