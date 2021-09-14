import numpy as np      #import needed modules
from scipy.io.wavfile import write     
import pyaudio
import wave

from soundUtils import SoundUtils

class Synth():

    filenames = {}
    sps = 44100
    duration_s = 0.5
    max_range = 32767
    filename_prefix = "NOTE_"
    filename_extension = ".wav"
    chunk_size = 1024
    # sound_utils = SoundUtils()
    p = pyaudio.PyAudio()


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

        # self.filenames[wavfile_name] = wave.open(wavfile_name, "rb")
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
        

        note_files = self.filenames.values()

        while True:
            print(self.filenames.keys())
            # if len(note_files) == 0: return
            for file in note_files:
                file_buffer = file.readframes(self.chunk_size)
                if len(file_buffer) <= 0:
                    file.rewind()
                    file_buffer = file.readframes(2)
                    file_buffer = file.readframes(self.chunk_size)
                float32_array_from_buffer = np.frombuffer(file_buffer, dtype=np.int16).astype(np.float32)
                if len(float32_array_from_buffer) < self.chunk_size: 
                    file.rewind()
                    file_buffer = file.readframes(self.chunk_size - len(float32_array_from_buffer))
                    buffer_complement = np.frombuffer(file_buffer, dtype=np.int16).astype(np.float32)
                    # print("COMPLEMENT")
                    print(base_waveform)
                    slice_index = np.argmax(buffer_complement < float32_array_from_buffer[len(float32_array_from_buffer)-1])
                    float32_array_from_buffer = np.concatenate([float32_array_from_buffer, buffer_complement[slice_index:]])
                    if len(float32_array_from_buffer) < self.chunk_size:
                        
                        file_buffer = file.readframes(self.chunk_size - len(float32_array_from_buffer))
                        buffer_complement = np.frombuffer(file_buffer, dtype=np.int16).astype(np.float32)
                        float32_array_from_buffer = np.concatenate([float32_array_from_buffer, buffer_complement])
                    # file.rewind()
                base_waveform = base_waveform + float32_array_from_buffer
            # if base_waveform:
            base_waveform = np.int16(self.squishify(base_waveform))
            # print("FINAL CHUNK: {}".format(base_waveform))
            base_waveform = base_waveform.tobytes()
            
            stream.write(base_waveform)
            base_waveform = np.zeros(self.chunk_size, np.float32)

    def get_file_pointers(self):
        pointers = []

        for name in self.filenames:
            current_pointer = wave.open(name, "rb")
            pointers.append(current_pointer)
        
        return pointers
    
    def removeFilePointer(self, index):
        del self.filenames[index]

    def addFilePointer(self, filename):
        self.filenames[filename] = wave.open(filename, "rb")