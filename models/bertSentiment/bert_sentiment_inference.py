from transformers import BertTokenizer, TFBertForSequenceClassification
# import tensorflow as tf

# tokenizer = BertTokenizer.from_pretrained("berturk-sentiment-model")
# model = TFBertForSequenceClassification.from_pretrained('berturk-sentiment-model', num_labels=2)


def predict_sentiment(text, tokenizer=None, model=None):
    return text
    # inputs = tokenizer(text, return_tensors="tf", padding=True, truncation=True)
    # outputs = model(**inputs)
    # predictions = tf.nn.softmax(outputs.logits, axis=-1)
    # predicted_label = tf.argmax(predictions, axis=1).numpy()[0]
    # return predicted_label

text = "Bu adam bir pislik."
print(predict_sentiment(text))
