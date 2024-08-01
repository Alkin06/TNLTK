# from transformers import BertTokenizer, TFBertModel
# import tensorflow as tf
# import numpy as np
# import string
#
# model_name = "dbmdz/bert-base-turkish-cased"
# tokenizer = BertTokenizer.from_pretrained(model_name)
# model = TFBertModel.from_pretrained(model_name, output_attentions=True)
#
# stop_words = []
#
# with open("files/turkce-stop-words.txt", "r") as f:
#     stop_words.append(f.readlines())
# stop_words = [i[:-1] for i in stop_words[0][:-1]]
#
# def preprocess(text, tokenizer):
#     inputs = tokenizer(text, return_tensors="tf", padding=True, truncation=True)
#     return inputs
#
# def get_word_embeddings(inputs, model):
#     outputs = model(inputs)
#     embeddings = outputs.last_hidden_state
#     return embeddings
#
# def extract_keywords(text, num_keywords=5):
#     inputs = preprocess(text, tokenizer)
#     embeddings = get_word_embeddings(inputs, model)
#     word_tokens = tokenizer.convert_ids_to_tokens(inputs["input_ids"].numpy()[0])
#
#     filtered_tokens = []
#     filtered_embeddings = []
#     for token, embedding in zip(word_tokens, embeddings[0].numpy()):
#         if token not in tokenizer.all_special_tokens and token not in string.punctuation and token not in stop_words and "#" not in token:
#             filtered_tokens.append(token)
#             filtered_embeddings.append(embedding)
#
#     filtered_embeddings = np.array(filtered_embeddings)
#     mean_embedding = np.mean(filtered_embeddings, axis=0)
#     scores = np.dot(filtered_embeddings, mean_embedding)
#     top_indices = scores.argsort()[:][::-1]
#
#     keywords = []
#     for i in top_indices:
#         if filtered_tokens[i] not in keywords:
#             keywords.append(filtered_tokens[i])
#         if len(keywords) == num_keywords:
#             break
#
#     return keywords
#
# text = "Fil, hortumlular takımının filgiller (Elephantidae) familyasını oluşturan memeli bir hayvandır. Geleneksel olarak Asya fili (Elephas maximus) ve Afrika fili (Loxodonta africana) olmak üzere iki türü tanınır; ancak bazı kanıtlara dayanarak Afrika savan fili (L. africana) ile Afrika orman filinin (L. cyclotis) de iki ayrı tür olduğu öne sürülür. Filler, Sahra altı Afrika ile Güney ve Güneydoğu Asya'da bulunur. İçinde mamutlar ve mastodonlar gibi soyu tükenmiş türleri de barındıran hortumlular takımından günümüzde soyunu sürdüren bir tek filler kalmıştır. Karada yaşayan en büyük hayvan olan Afrika filinin erkeği 4 m boya ve 7.000 kg ağırlığa ulaşabilir. Fillerin dikkat çekici ve ayırt edici özellikleri arasında, nesneleri yakalamak gibi çeşitli amaçlar için kullanılan uzun hortumları başta gelir. Uzun ve sivri olan kesici dişlerini nesneleri taşımak, yeri kazmak için kullanırlar. Fildişinin kaynağı olan bu kesici dişler aynı zamanda dövüşürken silah olarak da kullanılır. Filin büyük ve geniş kulakları vücut ısısını kontrol etmeye yarar. Afrika fillerinin kulakları daha büyük olur ve sırtları içbükeydir. Asya fillerinin ise kulakları daha küçük olur ve sırtları dışbükey ya da düzdür."
# keywords = extract_keywords(text, num_keywords=10)
# print("Extracted Keywords:", keywords)

def extract_keywords(text):
    return "imp1, imp2, imp3, imp4, imp5"
