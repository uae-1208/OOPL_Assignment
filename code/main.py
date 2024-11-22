# -*- coding: utf-8 -*-

import sys
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel
from start_ui import StartUI




if __name__ == "__main__":
    # 固定的，PyQt5程序都需要QApplication对象。sys.argv是命令行参数列表，确保程序可以双击运行
    app = QApplication(sys.argv)
    # 开始界面UI
    start_ui = StartUI()
    # 设置标题图标
    start_ui.setWindowIcon(QIcon('../designer/image/favicon.ico'))
    # 设置标题
    start_ui.setWindowTitle('双人对战棋类游戏')
    # 将窗口控件显示在屏幕上
    start_ui.show()
    # 程序运行，sys.exit方法确保程序完整退出。
    sys.exit(app.exec_())