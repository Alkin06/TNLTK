from transformers import BertTokenizer, TFBertModel
import tensorflow as tf
import numpy as np
import string

model_name = "models/bertTurkishBased/berturkModel"
tokenizer = BertTokenizer.from_pretrained(model_name)
model = TFBertModel.from_pretrained(model_name, output_attentions=True)

stop_words = []

with open("models/bertTurkishBased/turkce-stop-words.txt", "r") as f:
    stop_words.append(f.readlines())
stop_words = [i[:-1] for i in stop_words[0][:-1]]

def preprocess(text, tokenizer):
    inputs = tokenizer(text, return_tensors="tf", padding=True, truncation=True)
    return inputs

def get_word_embeddings(inputs, model):
    outputs = model(inputs)
    embeddings = outputs.last_hidden_state
    return embeddings

def extract_keywords(text, num_keywords=5):
    inputs = preprocess(text, tokenizer)
    embeddings = get_word_embeddings(inputs, model)
    word_tokens = tokenizer.convert_ids_to_tokens(inputs["input_ids"].numpy()[0])

    filtered_tokens = []
    filtered_embeddings = []
    for token, embedding in zip(word_tokens, embeddings[0].numpy()):
        if token not in tokenizer.all_special_tokens and token not in string.punctuation and token not in stop_words and "#" not in token:
            filtered_tokens.append(token)
            filtered_embeddings.append(embedding)

    filtered_embeddings = np.array(filtered_embeddings)
    mean_embedding = np.mean(filtered_embeddings, axis=0)
    scores = np.dot(filtered_embeddings, mean_embedding)
    top_indices = scores.argsort()[:][::-1]

    keywords = []
    for i in top_indices:
        if filtered_tokens[i] not in keywords:
            keywords.append(filtered_tokens[i])
        if len(keywords) == num_keywords:
            break

    return ",".join(keywords)
