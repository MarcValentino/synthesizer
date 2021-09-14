import numpy as np
from scipy.io.wavfile import write     
import pyaudio
import wave

class SoundUtils():

    max_range = 32767
    sps = 44100
    duration_s = 0.5
    max_range = 32767
    filename_prefix = "NOTE_"
    filename_extension = ".wav"
    chunk_size = 1024

    def synthesizeNote(self, frequency, c1, c2, c3, c4):
        sample_number = np.arange(int(self.duration_s*frequency)* self.sps)
        wavfile_name = self.filename_prefix + str(frequency) + "-" + str(c1) + "-" + str(c2) + "-" + str(c3) + "-" + str(c4) + self.filename_extension
        try:
            file_test = wave.open(wavfile_name)
            file_test.close()
        except:

            waveform = 0.10 * np.sin((2*np.pi * sample_number*frequency)/self.sps) * self.max_range
            waveform2 = 0.10 * np.sin((2*2*np.pi * sample_number*frequency)/self.sps) * self.max_range
            waveform3 = 0.10 * np.sin((3*2*np.pi * sample_number*frequency)/self.sps) * self.max_range
            waveform4 = 0.10 * np.sin((4*2*np.pi * sample_number*frequency)/self.sps) * self.max_range
            base_waveform = c1*waveform + c2*waveform2 + c3*waveform3 + c4*waveform4
            base_waveform_int16 = np.int16(self.squishify(base_waveform))
            
            write(wavfile_name, self.sps, base_waveform_int16)

        # self.filenames.append(wave.open(wavfile_name, "rb"))
        return wave.open(wavfile_name)

    def squishify(self, sample_array):
        max_value = int(np.amax(np.abs(sample_array)))
        # print("MAX_VALUE: " + str(max_value))
        if max_value >= self.max_range:
            squish_ratio = self.max_range / max_value
            return sample_array * squish_ratio
        return sample_array 