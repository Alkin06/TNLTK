import os
import sys
import tempfile
import time
import wave
import librosa
import numpy as np
import soundfile as sf
import torch
from espnet2.bin.asr_inference import Speech2Text


def convert_to_wav(input_file, target_sample_rate=16000):
    # Load audio file using librosa
    y, sr = librosa.load(input_file, sr=target_sample_rate)
    temp_wav = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    sf.write(temp_wav.name, y, target_sample_rate, format='WAV', subtype='PCM_16')
    return temp_wav.name


def recognize(wavfile, device, speech2text):
    wavfile = convert_to_wav(wavfile, target_sample_rate=16000)
    timer = time.perf_counter()
    with wave.open(wavfile, 'rb') as wavfile:
        ch = wavfile.getnchannels()
        bits = wavfile.getsampwidth()
        rate = wavfile.getframerate()
        nframes = wavfile.getnframes()
        buf = wavfile.readframes(-1)
        data = np.frombuffer(buf, dtype='int16')
    speech = data.astype(
        np.float16) / 32767.0
    speech_tensor = torch.tensor(speech, device=device)

    results = speech2text(speech_tensor)
    print('time passed:', time.perf_counter() - timer)
    print("RECOGNIZED", results[0][0])
    return results[0][0], time.perf_counter() - timer


def main(wav_file):
    current_directory = os.getcwd()
    relative_path = "../TNLTK/models/TurkicASR/turkic_languages_model/"
    absolute_path = os.path.abspath(relative_path)
    os.chdir(absolute_path)
    sys.path.append(absolute_path)
    sys.path.append(absolute_path + "/exp/")
    print(sys.path)
    if os.path.exists(wav_file):
        asr_model_path = absolute_path + "/exp/asr_train_asr_1410_raw_all_turkic_1610_char_sp"
        lm_model_path = absolute_path + "/exp/lm_train_lm_1410_all_turkic_1610_char"

        train_config = asr_model_path + "/config.yaml"
        model_file = asr_model_path + "/valid.acc.ave_10best.pth"

        lm_config = lm_model_path + "/config.yaml"
        lm_file = lm_model_path + "/valid.loss.ave_10best.pth"
        device = "cuda" if torch.cuda.is_available() else "cpu"


        speech2text = Speech2Text(
            asr_train_config=train_config,
            asr_model_file=model_file,
            lm_train_config=lm_config,
            lm_file=lm_file,
            token_type=None,
            bpemodel=None,
            maxlenratio=0.0,
            minlenratio=0.0,
            beam_size=10,
            ctc_weight=0.5,
            lm_weight=0.3,
            penalty=0.0,
            nbest=1,
            device=device
        )
        os.chdir(current_directory)
        return recognize(wav_file, device, speech2text)
