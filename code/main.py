# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel
from win_ctrl import WindowContorller
from MACRO import *








if __name__ == "__main__":
    # 固定的，PyQt5程序都需要QApplication对象。sys.argv是命令行参数列表，确保程序可以双击运行
    app = QApplication(sys.argv)

    win_ctrl = WindowContorller()
    # 打开登录界面UI
    win_ctrl.switch_win(OPEN_LOGIN)

    # 程序运行，sys.exit方法确保程序完整退出。
    sys.exit(app.exec_())