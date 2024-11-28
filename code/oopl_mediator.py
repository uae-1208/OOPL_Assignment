from go_ui import GoUI
from gobang_ui import GobangUI

CLOSE = 0
OPEN = 1


# 中介，用来协调窗口切换
class Mediator:
    def __init__(self):
        self.start_win = None
        self.game_win = None

    def notify(self, sender, event):
        if sender == "START":
            self.game_win.method(event)
        elif sender == "GAME":
            self.start_win.call_method(event)


# 开始窗口
class START_WINDOW:
    def __init__(self, mediator, win):
        self.mediator = mediator
        self.mediator.start_win = self
        self.win = win      # go_ui或者gobang_ui的实例

    def call_method(self, event):
        if event == CLOSE:
            self.win.close()
        elif event == OPEN:
            self.win.show()

    # 发送事件
    def send_event(self, event):
        self.mediator.notify("START", event)


# 棋类游戏窗口
class GAME_WINDOW:
    def __init__(self, mediator, win):
        self.mediator = mediator
        self.mediator.game_win = self
        self.win = win      # go_ui或者gobang_ui的实例

    def method(self, event):
        if event == CLOSE:
            self.win.close()
        elif event == OPEN:
            self.win.show()

    # 发送事件
    def send_event(self, event):
        self.mediator.notify("GAME", event)


