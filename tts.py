# -*- coding: utf-8 -*-
from bingtts import Translator
import wave
import pyaudio
def tts(text):
    translator = Translator('b2efca95d4b74c3ca0d1e5b0729963fe')
    output = translator.speak(text, "en-US", "Male", "riff-16khz-16bit-mono-pcm")
    # print(type(output))
    with open("file.wav", "w") as f:
        f.write(output)
    chunk = 1024
    wf = wave.open(r"file.wav", 'rb')

    p = pyaudio.PyAudio()
    stream = p.open(format = p.get_format_from_width(wf.getsampwidth()),
                    channels = wf.getnchannels(),
                    rate = wf.getframerate(),
                    output = True)
    while True:
        data = wf.readframes(chunk)
        if data == "": break
        stream.write(data)
    stream.close()
    p.terminate()

tts("Welcome")