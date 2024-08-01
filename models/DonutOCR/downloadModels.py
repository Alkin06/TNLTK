from transformers import DonutProcessor, VisionEncoderDecoderModel, MarianMTModel, MarianTokenizer

model_name = "naver-clova-ix/donut-base-finetuned-cord-v2"
processor = DonutProcessor.from_pretrained(model_name)
model = VisionEncoderDecoderModel.from_pretrained(model_name)

translation_model_name = "Helsinki-NLP/opus-mt-tc-big-en-tr"
translation_model = MarianMTModel.from_pretrained(translation_model_name)
translation_tokenizer = MarianTokenizer.from_pretrained(translation_model_name)

processor.save_pretrained("./donut_processor")
model.save_pretrained("./donut_model")
translation_model.save_pretrained("./translation_model")
translation_tokenizer.save_pretrained("./translation_tokenizer")
