"""
    # Конвертация файлов из mp3 в wav
    # Два варианта
    # 1) библиотека AudioSegment
    from pydub import AudioSegment

    # files
    src = "audio.mp3"
    dst = "audio.wav"

    # convert wav to mp3
    sound = AudioSegment.from_mp3(src)
    sound.export(dst, format="wav")

    # 2) использовать subprocess
    import subprocess

    # convert mp3 to wav file
    subprocess.call(['ffmpeg', '-i', 'audio.mp3', 'converted_to_wav_file.wav'])

"""

import speech_recognition as sr

FILE = 'audio.wav'

r = sr.Recognizer()
with sr.AudioFile(FILE) as source:
    audio = r.record(source)  # read the entire audio file

try:
    text = r.recognize_google(audio, language='ru-RU')
    print(text)
except sr.UnknownValueError:
    print("Google Speech Recognition could not understand audio")
except sr.RequestError as e:
    print(f"Could not request results"
          f" from Google Speech Recognition service; {e}")
