# from transformers import BertTokenizer, TFBertModel
# import tensorflow as tf
# import numpy as np
#
# model_name = "dbmdz/bert-base-turkish-cased"
# tokenizer = BertTokenizer.from_pretrained(model_name)
# model = TFBertModel.from_pretrained(model_name)
#
# def get_sentence_embeddings(text, tokenizer, model):
#     sentences = text.split('. ')
#     sentences = [sentence.strip() for sentence in sentences if sentence.strip()]
#     inputs = tokenizer(sentences, return_tensors="tf", padding=True, truncation=True)
#     outputs = model(**inputs)
#     embeddings = outputs.last_hidden_state
#     sentence_embeddings = tf.reduce_mean(embeddings, axis=1)
#     return sentences, sentence_embeddings
#
# def rank_sentences(sentences, embeddings):
#     mean_embedding = tf.reduce_mean(embeddings, axis=0)
#     similarities = []
#     for sentence, embedding in zip(sentences, embeddings):
#         similarity = tf.reduce_sum(mean_embedding * embedding)
#         similarities.append((sentence, similarity))
#     ranked_sentences = sorted(similarities, key=lambda x: x[1], reverse=True)
#     return ranked_sentences
#
# def extractive_summary(text, target_percentage=0.3):
#     sentences, embeddings = get_sentence_embeddings(text, tokenizer, model)
#     ranked_sentences = rank_sentences(sentences, embeddings)
#     target_length = int(len(sentences) * target_percentage)
#     selected_sentences = []
#     current_length = 0
#     for sentence, _ in ranked_sentences:
#         selected_sentences.append(sentence)
#         current_length += 1
#         if current_length >= target_length:
#             break
#     summary = '. '.join(selected_sentences) + "."
#     return summary
# text = "Fil, hortumlular takımının filgiller (Elephantidae) familyasını oluşturan memeli bir hayvandır. Geleneksel olarak Asya fili (Elephas maximus) ve Afrika fili (Loxodonta africana) olmak üzere iki türü tanınır; ancak bazı kanıtlara dayanarak Afrika savan fili ile Afrika orman filinin de iki ayrı tür olduğu öne sürülür. Filler, Sahra altı Afrika ile Güney ve Güneydoğu Asya'da bulunur. İçinde mamutlar ve mastodonlar gibi soyu tükenmiş türleri de barındıran hortumlular takımından günümüzde soyunu sürdüren bir tek filler kalmıştır. Karada yaşayan en büyük hayvan olan Afrika filinin erkeği 4 m boya ve 7.000 kg ağırlığa ulaşabilir. Fillerin dikkat çekici ve ayırt edici özellikleri arasında, nesneleri yakalamak gibi çeşitli amaçlar için kullanılan uzun hortumları başta gelir. Uzun ve sivri olan kesici dişlerini nesneleri taşımak, yeri kazmak için kullanırlar. Fildişinin kaynağı olan bu kesici dişler aynı zamanda dövüşürken silah olarak da kullanılır. Filin büyük ve geniş kulakları vücut ısısını kontrol etmeye yarar. Afrika fillerinin kulakları daha büyük olur ve sırtları içbükeydir. Asya fillerinin ise kulakları daha küçük olur ve sırtları dışbükey ya da düzdür."
# summary = extractive_summary(text, target_percentage=0.5)
# print(summary)

def extractive_summary(text):
    return text