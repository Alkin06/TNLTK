import torch
from transformers import pipeline
import os

os.environ["TRANSFORMERS_VERBOSITY"] = "error"
pipe = pipeline("text-generation", model="asafaya/kanarya-2b", device_map = "auto")

def generate_response(question):
    messages = [{"role": "user", "content": question}]
    response = pipe(messages, max_new_tokens=128)[0]['generated_text'][-1]
    return response
