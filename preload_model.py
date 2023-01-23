"""Base server."""
import torch
from transformers import (
    GPT2LMHeadModel,
    GPT2Tokenizer
)

device = torch.device("cpu")
model_class, tokenizer_class = (
GPT2LMHeadModel,
GPT2Tokenizer
)
tokenizer = tokenizer_class.from_pretrained(
    'sberbank-ai/rugpt3medium_based_on_gpt2'
)
model = model_class.from_pretrained(
    'sberbank-ai/rugpt3medium_based_on_gpt2'
)
model.to(device)
