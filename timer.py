import time
from PyQt5.QtCore import QThread, pyqtSignal


#对局时间线程
class GameTime(QThread):
    _signal = pyqtSignal(str)

    def __init__(self,label):
        self.label = label
        super(GameTime, self).__init__()

    def set_status(self,status):
        self.status = status

    def run(self):
        start = time.time()
        while self.status:
            time.sleep(1)
            end = time.time()
            second = int(end-start)
            display_time = str(int(second/60))+":"+str(second%60)
            #print(display_time)
            self._signal.emit(display_time)