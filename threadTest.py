from threading import Thread
from synth import Synth
import time

class ThreadedSynth(Synth, Thread):

    def run(self):
        self.play()

if __name__ == '__main__':
    threaded_synth = ThreadedSynth()

    base_frequency = 200
    ratio = 1.05946
    filename_1st = threaded_synth.synthesizeNote(base_frequency, 1, 0.7, 0.8, 0.3) #só toma cuidado que por agora synth.play() morre se você não tiver nota alguma tocando
    threaded_synth.start()
    time.sleep(1)
    filename_3rd = threaded_synth.synthesizeNote(base_frequency * (ratio **4), 1, 0.7, 0.8, 0.3)
    time.sleep(1)
    filename_5th = threaded_synth.synthesizeNote(base_frequency * (ratio **7), 1, 0.7, 0.8, 0.3)