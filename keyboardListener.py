from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import *
from threadTest import ThreadedSynth
from threading import Thread

class KeyboardListener(QWidget):

    bindings = {}

    def __init__(self):
        # sintetizar as notas (se necessário)
        super().__init__()
        self.threadedSynth = ThreadedSynth()
        self.FtoPayRespects = self.threadedSynth.synthesizeNote(174.61, 0.7, 0.8, 0.3, 0.2)
        self.threadedSynth.start()
        self.GtoPaySomeMoney = self.threadedSynth.synthesizeNote(174.61 * (1.05946**2), 0.7, 0.8, 0.3, 0.2)
        # associar cada nota sintetizada a uma tecla
        # iniciar uma instância de ThreadedSynth em uma thread separada
        return

    def event(self, event):
        if event.type() == QEvent.KeyPress:
            # procurar a nota associada a tecla que foi pressionada/solta
            # adicionar à lista de ponteiros do ThreadedSynth a nota
            if not event.isAutoRepeat(): 
                if event.key() == 70: self.threadedSynth.addFilePointer(self.FtoPayRespects)
                if event.key() == 71: self.threadedSynth.addFilePointer(self.GtoPaySomeMoney)
            print("KEY PRESSED: {}\nTYPE: {}".format(event.key(), type(event.key()))) 
            return True

        if event.type() == QEvent.KeyRelease:
            # procurar a nota associada a tecla que foi pressionada/solta
            if not event.isAutoRepeat(): 
                if event.key() == 70: self.threadedSynth.removeFilePointer(self.FtoPayRespects)
                if event.key() == 71: self.threadedSynth.removeFilePointer(self.GtoPaySomeMoney)
            print("KEY RELEASED: {}\nTYPE: {}".format(event.key(), type(event.key())))
            # remover da lista de ponteiros do ThreadedSynth a nota
            return True
        
        return super().event(event)