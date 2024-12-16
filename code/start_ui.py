from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5.QtGui import QIcon, QIntValidator
from MACRO import *
from gobang_ui import GobangUI
from go_ui import GoUI
from othello_ui import OthelloUI
from start_qt import Ui_StartWindow



class StartUI(QMainWindow, Ui_StartWindow):
    def __init__(self, parent=None, wc=None):
        super(StartUI, self).__init__(parent)
        self.setupUi(self)
        self.win_ctrl = wc

        # 设置sizeInput的验证器：只允许输入 0 到 100 的整数
        int_validator = QIntValidator(0, 100, self)
        self.sizeInput.setValidator(int_validator)
        # 点击“开始游戏”
        self.startButton.clicked.connect(self.start_game)


    def start_game(self):
        # 检测是否检测输入了size
        context = self.sizeInput.text()
        if context == "":
            QMessageBox.information(self, "提示", "请输入棋盘尺寸！")
            return

        # 检测输入的size是否符合要求
        size = int(context)
        if size<8 or size>19:
            QMessageBox.information(self, "提示", "棋盘尺寸设置不合理！")
            return

        current_chess = self.combBox.currentIndex()
        if current_chess == GOBANG :
            self.win_ctrl.switch_win(START_2_GOBANG)
        elif current_chess == GO :
            self.win_ctrl.switch_win(START_2_GO)
        elif current_chess == OTHELLO :
            self.win_ctrl.switch_win(START_2_OTHELLO)
        else:
            raise Exception("Wrong!")


    # 重写 closeEvent，当用户点击关闭按钮时自动返回到登录界面
    def closeEvent(self, event):
        self.win_ctrl.switch_win(START_2_LOGIN)
