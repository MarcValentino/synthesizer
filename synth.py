import numpy as np      #import needed modules
from scipy.io.wavfile import write     #sudo apt-get install python-pyaudio
import pyaudio
import wave
import time

class Synth():

    filenames = []
    sps = 44100
    duration_s = 5
    max_range = 32767
    filename_prefix = "NOTE_"
    filename_extension = ".wav"
    chunk_size = 1024

    p = pyaudio.PyAudio()

    def synthesizeNote(self, frequency, c1, c2, c3, c4):
        period = 1/frequency
        sample_number = np.arange(self.duration_s* self.sps)

        waveform = 0.3 * np.sin((2*np.pi * sample_number/period)/self.sps) * self.max_range
        waveform2 = 0.3 * np.sin((2*2*np.pi * sample_number/period )/self.sps) * self.max_range
        waveform3 = 0.3 * np.sin((3*2*np.pi * sample_number/period )/self.sps) * self.max_range
        waveform4 = 0.3 * np.sin((4*2*np.pi * sample_number/period )/self.sps) * self.max_range
        final_waveform = c1*waveform + c2*waveform2 + c3*waveform3 + c4*waveform4
        final_waveform_int16 = np.int16(self.squishify(final_waveform))
        wavfile_name = self.filename_prefix + str(frequency) + "-" + str(c1) + "-" + str(c2) + "-" + str(c3) + "-" + str(c4) + self.filename_extension
        write(wavfile_name, self.sps, final_waveform_int16)
        self.filenames.append(wavfile_name)
        return wavfile_name

    def squishify(self, sample_array):
        max_value = int(np.amax(np.abs(sample_array)))
        # print("MAX_VALUE: " + str(max_value))
        if max_value >= self.max_range:
            squish_ratio = self.max_range / max_value
            return sample_array * squish_ratio
        return sample_array 
    
    def play(self):
        base_waveform = np.zeros(self.chunk_size, np.float32)

        stream = self.p.open(format=self.p.get_format_from_width(2),
                    channels=1,
                    rate=self.sps,
                    output=True)
        

        note_files = self.get_file_pointers()

        while True:
            final_waveform = base_waveform
            for file in note_files:
                file_buffer = file.readframes(self.chunk_size)
                if len(file_buffer) <= 0:
                    file.rewind()
                    file_buffer = file.readframes(self.chunk_size)
                float32_array_from_buffer = np.frombuffer(file_buffer, dtype=np.int16).astype(np.float32)
                if len(float32_array_from_buffer) < self.chunk_size:
                    file.rewind()
                    file_buffer = file.readframes(self.chunk_size - len(float32_array_from_buffer))
                    buffer_complement = np.frombuffer(file_buffer, dtype=np.int16).astype(np.float32)
                    print("COMPLEMENT")
                    
                    float32_array_from_buffer = np.concatenate([float32_array_from_buffer, buffer_complement])
                    # file.rewind()
                final_waveform = final_waveform + float32_array_from_buffer
            
            final_waveform = np.int16(self.squishify(final_waveform))
            final_waveform = final_waveform.tobytes()

            stream.write(final_waveform)


    def get_file_pointers(self):
        pointers = []

        for name in self.filenames:
            current_pointer = wave.open(name, "rb")
            pointers.append(current_pointer)
        
        return pointers
    
if __name__ == '__main__':

    synth = Synth()
    ratio = 1.05946
    base_frequency = 125
    filename_1st = synth.synthesizeNote(base_frequency, 1, 0.5, 0.25, 0.125)
    filename_3rd = synth.synthesizeNote(base_frequency * (ratio **4), 1, 0.5, 0.25, 0.125)
    filename_5th = synth.synthesizeNote(base_frequency * (ratio **7), 1, 0.5, 0.25, 0.125)
    synth.play()
    