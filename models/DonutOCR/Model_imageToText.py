import os
import shutil
import sys
from turkishnlp import detector
import torch
from PIL import Image

from transformers import DonutProcessor, VisionEncoderDecoderModel, MarianMTModel, MarianTokenizer
import re


def loadModels():
    processor = DonutProcessor.from_pretrained("./models/DonutOCR/donut_processor")
    model = VisionEncoderDecoderModel.from_pretrained("./models/DonutOCR/donut_model")

    translation_model = MarianMTModel.from_pretrained("./models/DonutOCR/translation_model")
    translation_tokenizer = MarianTokenizer.from_pretrained("./models/DonutOCR/translation_tokenizer")
    return processor, model, translation_model, translation_tokenizer


def translate_text(text, translation_model, translation_tokenizer):
    translated = translation_model.generate(
        **translation_tokenizer(text, padding=True, return_tensors="pt"))
    for t in translated:
        print(translation_tokenizer.decode(t, skip_special_tokens=True))
    print(translation_tokenizer.decode(translated[0], skip_special_tokens=True))
    return translation_tokenizer.decode(translated[0], skip_special_tokens=True)


def process_image(image_path, processor, model):
    image = Image.open(image_path)
    image = image.convert("RGB")
    pixel_values = processor(image, return_tensors="pt").pixel_values
    print(pixel_values.shape)

    task_prompt = "<s_cord-v2>"
    decoder_input_ids = processor.tokenizer(task_prompt, add_special_tokens=False, return_tensors="pt")["input_ids"]

    device = "cuda" if torch.cuda.is_available() else "cpu"
    model.to(device)

    outputs = model.generate(pixel_values.to(device),
                             decoder_input_ids=decoder_input_ids.to(device),
                             max_length=model.decoder.config.max_position_embeddings,
                             early_stopping=True,
                             pad_token_id=processor.tokenizer.pad_token_id,
                             eos_token_id=processor.tokenizer.eos_token_id,
                             use_cache=True,
                             num_beams=1,
                             bad_words_ids=[[processor.tokenizer.unk_token_id]],
                             return_dict_in_generate=True,
                             output_scores=True)

    sequence = processor.batch_decode(outputs.sequences, skip_special_tokens=True)[0]
    sequence = processor.batch_decode(outputs.sequences)[0]
    sequence = sequence.replace(processor.tokenizer.eos_token, "").replace(processor.tokenizer.pad_token, "")
    sequence = re.sub(r"<.*?>", "", sequence, count=1).strip()  # remove first task start token
    return sequence


def clean_text(ocr_text):
    # Removing unnecessary tags and cleaning up the text
    text = re.sub(r'<.*?>', '', ocr_text)  # Remove all tags
    text = re.sub(r'\s+', ' ', text)  # Normalize whitespace
    text = text.strip()  # Trim leading and trailing spaces
    return text


def __get_directory():
    """
        Return the target directory depending on the OS.
        """
    if sys.platform == 'win32' and 'APPDATA' in os.environ:
        homedir = os.environ['APPDATA']
    else:
        homedir = os.path.expanduser('~/')
        if homedir == '~/':
            raise ValueError("Could not find a default download directory")

    return os.path.join(homedir, 'TRnlpdata')


def move_files():
    """
        Move data files to the specific directory.
        """
    directory = __get_directory()

    if not os.path.exists(directory):
        os.makedirs(directory)

    project_files = [
        "models/DonutOCR/spellCheckerFiles/words.pkl",
        "models/DonutOCR/spellCheckerFiles/words_counted.pkl",
        "models/DonutOCR/spellCheckerFiles/words_alt.pkl"
    ]

    for file_path in project_files:
        file_name = os.path.basename(file_path)
        destination_path = os.path.join(directory, file_name)
        if not os.path.exists(destination_path):
            shutil.copy(file_path, destination_path)
        shutil.copy(file_path, destination_path)

    print("Files have been moved successfully")


def main(image_path):
    # image_path = "img.png"
    #current_directory = os.getcwd()
    #relative_path = "models/DonutOCR/"
    #absolute_path = os.path.abspath(relative_path)
    #os.chdir(relative_path)
    processor, model, translation_model, translation_tokenizer = loadModels()
    result_text = process_image(image_path, processor, model)

    cleaned_text = clean_text(result_text)
    print(cleaned_text)

    obj = detector.TurkishNLP()  # To spell check and figure out if the text is Turkish
    move_files()
    obj.create_word_set()

    if not obj.is_turkish(cleaned_text):
        cleaned_text = translate_text(cleaned_text, translation_model, translation_tokenizer)

    #lwords = obj.list_words(cleaned_text)
    # print(obj.auto_correct(lwords))
    #spellCheckedText = obj.auto_correct(lwords)
    #result_string = ' '.join(spellCheckedText)
    #os.chdir(current_directory)
    return cleaned_text

