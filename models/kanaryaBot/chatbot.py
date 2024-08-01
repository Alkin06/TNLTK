import torch
from transformers import pipeline
import os

os.environ["TRANSFORMERS_VERBOSITY"] = "error"

pipe = pipeline("text-generation", model="asafaya/kanarya-2b", device_map = "auto")

messages = [
    {"role": "user", "content": "10 - 2 işleminin sonucu kaçtır?"},
 ]

print(pipe(messages, max_new_tokens=128)[0]['generated_text'][-1])