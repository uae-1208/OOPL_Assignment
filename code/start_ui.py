from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5.QtGui import QIcon, QIntValidator
from MACRO import *
from go_ui import GoUI
from gobang_ui import GobangUI
from start_qt import Ui_StartWindow



class StartUI(QMainWindow, Ui_StartWindow):
    def __init__(self, parent=None):
        super(StartUI, self).__init__(parent)
        self.setupUi(self)

        # 点击“开始游戏”
        self.startButton.clicked.connect(self.start_game)
        # 设置sizeInput的验证器：只允许输入 0 到 100 的整数
        int_validator = QIntValidator(0, 100, self)
        self.sizeInput.setValidator(int_validator)



    def start_game(self):
        current_chess = self.combBox.currentIndex()

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

        if current_chess == GOBANG :
            # 五子棋UI
            self.gobang_ui = GobangUI()
            #设置标题图标
            self.gobang_ui.setWindowIcon(QIcon('../designer/image/favicon.ico'))
            #设置标题
            self.gobang_ui.setWindowTitle('五子棋双人对战')
            self.gobang_ui.show()
        elif current_chess == GO :
            # 围棋UI
            self.go_ui = GoUI()
            #设置标题图标
            self.go_ui.setWindowIcon(QIcon('../designer/image/favicon.ico'))
            #设置标题
            self.go_ui.setWindowTitle('围棋双人对战')
            self.go_ui.show()


