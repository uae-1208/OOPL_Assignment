from go_ui import GoUI
from gobang_ui import GobangUI

GOBANG = 1  # 五子棋
GO = 2      # 围棋

class Window:
    def __init__(self, type):
        self.type = type    # 内部状态，共享部分。Go or Gobang
        if type == GOBANG:
            self.game_win = GobangUI()
        elif type == GO:
            self.game_win = GoUI()

    # 返回游戏窗口
    def get_game_win(self):
        return self.game_win


class WindowFactory:
    # 享元工厂，用于创建和管理共享的Window对象
    _windows = {}

    @staticmethod
    def get_window(window):
        # 如果不存在window类型的游戏窗口，则创建1个
        if window not in WindowFactory._windows:
            WindowFactory._windows[window] = Window(window)

        return WindowFactory._windows[window]


