import numpy as np      #import needed modules
from scipy.io.wavfile import write     #sudo apt-get install python-pyaudio
import pyaudio
import wave
import time
from pynput.keyboard import Listener

sps = 44100
freq_hz = 200.0
period = 1/freq_hz
duration_s = 100*period 

wavelength = duration_s * period

sample_number = np.arange(duration_s * sps)

waveform = 0.4 * np.sin((2*np.pi * sample_number/period)/sps) * 32767

waveform2 = 0.4 * np.sin((2*2*np.pi * sample_number/period )/sps) * 32767

waveform3 = 0.4 * np.sin((3*2*np.pi * sample_number/period )/sps) * 32767

waveform4 = 0.4 * np.sin((4*2*np.pi * sample_number/period )/sps) * 32767

final_waveform = np.int16(0.5*waveform + 0.3*waveform2 + 0.5*waveform3 + 0.3*waveform4)

write("note.wav", sps, final_waveform)

wf = wave.open("note.wav", "rb")

CHUNK = 1024

p = pyaudio.PyAudio()

stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate=wf.getframerate(),
                output=True)


data = wf.readframes(CHUNK)


while True:
        
    stream.write(data)
    if len(data) <= 0:
        wf.rewind()
    data = wf.readframes(CHUNK)
     
        