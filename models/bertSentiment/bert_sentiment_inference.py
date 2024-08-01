from transformers import BertTokenizer, TFBertForSequenceClassification
import tensorflow as tf

tokenizer = BertTokenizer.from_pretrained("models/bertSentiment/bertSentimentModel")
model = TFBertForSequenceClassification.from_pretrained('models/bertSentiment/bertSentimentModel', num_labels=2)


def predict_sentiment(text, tokenizer=tokenizer, model=model):
    inputs = tokenizer(text, return_tensors="tf", padding=True, truncation=True)
    outputs = model(**inputs)
    predictions = tf.nn.softmax(outputs.logits, axis=-1)
    predicted_label = tf.argmax(predictions, axis=1).numpy()[0]
    if predicted_label:
        result = "Positive"
    else:
        result = "Negative"
    return result
