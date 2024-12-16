from PyQt5.QtGui import QIcon, QPixmap
from login_ui import LogInUI
from register_ui import RegisterUI
from start_ui import StartUI
from gobang_ui import GobangUI
from go_ui import GoUI
from othello_ui import OthelloUI
from MACRO import *


# 窗口控制类
class WindowContorller:
    def __init__(self):

        self.set_player(0, 0)
        self.set_player_b_info(0, 0, 0, 0)
        self.set_player_w_info(0, 0, 0, 0)

        # 登录界面UI
        self.login_ui = LogInUI(wc=self)
        # 设置标题图标
        self.login_ui.setWindowIcon(QIcon('../designer/image/favicon.ico'))
        # 设置标题
        self.login_ui.setWindowTitle('登录界面')

        # 注册界面UI
        self.register_ui = RegisterUI(wc=self)
        # 设置标题图标
        self.register_ui.setWindowIcon(QIcon('../designer/image/favicon.ico'))
        # 设置标题
        self.register_ui.setWindowTitle('注册账号')

        # 开始界面UI
        self.start_ui = StartUI(wc=self)
        # 设置标题图标
        self.start_ui.setWindowIcon(QIcon('../designer/image/favicon.ico'))
        # 设置标题
        self.start_ui.setWindowTitle('棋类对战平台')




    # 交互两个棋手的相关：login_ui --> win_ctrl --> othello_ui
    # 设置两个棋手选择的玩家状态：账号用户/游客/一级AI/二级AI
    def set_player(self, player_w, player_b):
        self.player_w = player_w
        self.player_b = player_b
    # 返回两个棋手选择的玩家状态：账号用户/游客/一级AI/二级AI
    def get_player(self):
        return self.player_w, self.player_b
    # 设置黑棋的用户名、账号、总场次、胜场
    def set_player_b_info(self, username_b, act_b, AllPlays_b, WinPlays_b):
        self.username_b = username_b
        self.act_b = act_b
        self.AllPlays_b = AllPlays_b
        self.WinPlays_b = WinPlays_b
    # 返回黑棋的用户名、账号、总场次、胜场
    def get_player_b_info(self):
        return self.username_b, self.act_b, self.AllPlays_b, self.WinPlays_b
    # 设置白棋的用户名、账号、总场次、胜场
    def set_player_w_info(self, username_w, act_w, AllPlays_w, WinPlays_w):
        self.username_w = username_w
        self.act_w = act_w
        self.AllPlays_w = AllPlays_w
        self.WinPlays_w = WinPlays_w
    # 返回白棋的用户名、账号、总场次、胜场
    def get_player_w_info(self):
        return self.username_w, self.act_w, self.AllPlays_w, self.WinPlays_w



    # 切换窗口
    def switch_win(self, num):
        # 打开登录窗口
        if num == OPEN_LOGIN:
            self.login_ui.show()
        # 关闭登录窗口，打开注册窗口
        elif num == LOGIN_2_REGISTER:
            self.login_ui.hide()
            self.register_ui.show()
        # 关闭登录窗口，打开开始窗口
        elif num == LOGIN_2_START:
            self.login_ui.hide()
            self.start_ui.show()
        # 关闭注册窗口，打开登录窗口
        elif num == REGISTER_2_LOGIN:
            self.register_ui.hide()
            self.login_ui.show()
        # 关闭开始窗口，打开登录窗口
        elif num == START_2_LOGIN:
            self.start_ui.hide()
            self.login_ui.show()
        # 关闭开始窗口，打开黑白棋游戏窗口
        elif num == START_2_OTHELLO:
            # 新建一个黑白棋游戏窗口
            self.othello_ui = OthelloUI(wc=self)  # 黑白棋界面UI
            self.othello_ui.setWindowIcon(QIcon('../designer/image/favicon.ico'))  # 设置标题图标
            self.othello_ui.setWindowTitle('黑白棋对战')  # 设置标题
            self.start_ui.hide()
            self.othello_ui.show()
        # 关闭黑白棋游戏窗口，打开开始窗口
        elif num == OTHELLO_2_START:
            self.othello_ui.hide()
            self.start_ui.show()
        # 关闭开始窗口，打开五子棋游戏窗口
        elif num == START_2_GOBANG:
            # 新建一个五子棋游戏窗口、
            self.gobang_ui = GobangUI(wc=self)  # 五子棋UI
            self.gobang_ui.setWindowIcon(QIcon('../designer/image/favicon.ico'))    #设置标题图标
            self.gobang_ui.setWindowTitle('五子棋对战')    # 设置标题
            self.start_ui.hide()
            self.gobang_ui.show()
        # 关闭黑白棋游戏窗口，打开开始窗口
        elif num == GOBANG_2_START:
            self.gobang_ui.hide()
            self.start_ui.show()
        # 关闭开始窗口，打开围棋游戏窗口
        elif num == START_2_GO:
            # 新建一个围棋游戏窗口
            self.go_ui = GoUI(wc=self)  # 围棋UI
            self.go_ui.setWindowIcon(QIcon('../designer/image/favicon.ico'))    #设置标题图标
            self.go_ui.setWindowTitle('围棋对战')    # 设置标题
            self.start_ui.hide()
            self.go_ui.show()
        # 关闭围棋游戏窗口，打开开始窗口
        elif num == GO_2_START:
            self.go_ui.hide()
            self.start_ui.show()


