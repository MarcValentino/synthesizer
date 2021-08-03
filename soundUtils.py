import numpy as np
from scipy.io.wavfile import write     
import pyaudio
import wave

class SoundUtils():

    max_range = 32767

    def squishify(self, sample_array):
        max_value = int(np.amax(np.abs(sample_array)))
        # print("MAX_VALUE: " + str(max_value))
        if max_value >= self.max_range:
            squish_ratio = self.max_range / max_value
            return sample_array * squish_ratio
        return sample_array 