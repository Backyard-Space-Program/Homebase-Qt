import pyaudio
import wave
import sys
import time
import json
from modules.stdlib import *
from modules.log import *

audio_open = False
wave_file = None
wav_file = None
stream = None
times = None
py_audio = None

def open_audio(file):
    global audio_open, wave_file, stream, times, py_audio, wav_file
    log("opening audio, file = " + file)
    audio_open = True
    tcas = json.loads(readfile(file + "/info.json"))
    times = tcas["times"]
    wave_file = tcas["wav"]

    wav_file = wave.open(file + "/" + wave_file, "rb")

    py_audio = pyaudio.PyAudio()
    stream = py_audio.open(format=py_audio.get_format_from_width(wav_file.getsampwidth()),
                        channels=wav_file.getnchannels(),
                        rate=wav_file.getframerate(),
                        output=True)

def _play(sect):
    if not audio_open:
        log("error: audio is not yet open!", file = sys.stderr)
        return

    data = times[sect]
    start = data[0]
    end = data[1] # + 0.1
    length = end - start

    n_frames = int(start * wav_file.getframerate())
    wav_file.setpos(n_frames)

    n_frames = int(length * wav_file.getframerate())
    frames = wav_file.readframes(n_frames)
    stream.write(frames) # play audio

def play(*args):
    for sect in args:
        try:
            _play(sect)
        except KeyError:
            log("error: sound file not found: " + sect, file = sys.stderr)

def play_one(arg):
    try:
        _play(arg)
    except KeyError:
        log("error: sound file not found: " + sect, file = sys.stderr)

def close_audio():
    global audio_open
    log("closing audio")
    audio_open = False

    # delay?
    time.sleep(0.1)

    # close all streams
    stream.close()
    py_audio.terminate()
    wav_file.close()
