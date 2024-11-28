from PyQt5 import QtCore, QtGui, QtWidgets

# 产品类：游戏窗口的按钮
class GameBtn:
    def __init__(self):
        self.yeildBtn = None    # 投降
        self.retractBtn = None  # 悔棋一步
        self.restartBtn = None  # 重新开始
        self.giveuptBtn = None  # 弃一手
        self.storeBtn = None    # 保存棋局
        self.loadBtn = None     # 导入棋局



# 建造者类
class GameBtnBuilder:
    def __init__(self):
        self.btns = GameBtn()

    # 投降
    def set_yeildBtn(self, yeildBtn):
        self.btns.yeildBtn = yeildBtn
        return self

    # 悔棋一步
    def set_retractBtn(self, retractBtn):
        self.btns.retractBtn = retractBtn
        return self

    # 重新开始
    def set_restartBtn(self, restartBtn):
        self.btns.restartBtn = restartBtn
        return self

    # 弃一手
    def set_giveuptBtn(self, giveuptBtn):
        self.btns.giveuptBtn = giveuptBtn
        return self

    # 保存棋局
    def set_storeBtn(self, storeBtn):
        self.btns.storeBtn = storeBtn
        return self

    # 导入棋局
    def set_loadBtn(self, loadBtn):
        self.btns.loadBtn = loadBtn
        return self

    # 构造组件
    def build(self):
        return self.btns


# 指挥者类
class Director:
    # 五子棋按钮
    @staticmethod
    def build_gobang_btns(builder):
        return (builder.set_yeildBtn(QtWidgets.QPushButton())
                .set_retractBtn(QtWidgets.QPushButton())
                .set_restartBtn(QtWidgets.QPushButton())
                .set_storeBtn(QtWidgets.QPushButton())
                .set_loadBtn(QtWidgets.QPushButton())
                .build())

    # 围棋按钮：比五子棋多了一个“弃一手”按钮
    @staticmethod
    def build_go_btns(builder):
        return (builder.set_yeildBtn(QtWidgets.QPushButton())
                .set_retractBtn(QtWidgets.QPushButton())
                .set_restartBtn(QtWidgets.QPushButton())
                .set_giveuptBtn(QtWidgets.QPushButton())
                .set_storeBtn(QtWidgets.QPushButton())
                .set_loadBtn(QtWidgets.QPushButton())
                .build())


