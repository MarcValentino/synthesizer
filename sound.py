import numpy as np      #import needed modules
from scipy.io.wavfile import write     #sudo apt-get install python-pyaudio
import simpleaudio as sa

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
play_obj = sa.play_buffer(final_waveform, 1, 2, sps)

while True:
   if not play_obj.is_playing():
       play_obj = sa.play_buffer(final_waveform, 1, 2, sps)