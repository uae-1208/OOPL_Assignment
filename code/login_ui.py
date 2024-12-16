import os
from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon, QIntValidator
from MACRO import *
from login_qt import Ui_StartWindow




class LogInUI(QMainWindow, Ui_StartWindow):
    def __init__(self, parent=None, wc=None):
        super(LogInUI, self).__init__(parent)
        self.setupUi(self)
        self.win_ctrl = wc
        self.login_status_w = False
        self.login_status_b = False


        # 先隐藏两个棋手信息界面
        self.widget_b2.setGeometry(QtCore.QRect(50, 50, 0, 0))
        self.widget_w2.setGeometry(QtCore.QRect(380, 50, 0, 0))
        # 设置账号Input的验证器：账号必须是5位的数字，后续还要判断是否大于等于10000
        int_validator = QIntValidator(0, 99999, self)
        self.act_Input_b.setValidator(int_validator)
        self.act_Input_w.setValidator(int_validator)
        # 密码必须是长度不超过5位的数字
        self.pwd_Input_b.setValidator(int_validator)
        self.pwd_Input_w.setValidator(int_validator)
        # 改变玩家状态：账号用户/游客/一级AI/二级AI
        self.Box_b.currentIndexChanged.connect(self.change_player_b)
        self.Box_w.currentIndexChanged.connect(self.change_player_w)
        # 点击“登录黑/白棋账号”
        self.login_btn_b.clicked.connect(self.login_b)
        self.login_btn_w.clicked.connect(self.login_w)
        # 点击“退出黑棋/白账号”
        self.logout_btn_b.clicked.connect(self.logout_b)
        self.logout_btn_w.clicked.connect(self.logout_w)
        # 点击“注册账号”
        self.register_btn.clicked.connect(self.register)
        # 点击“开始游戏”
        self.start_btn.clicked.connect(self.start_game)



    # 改变黑棋玩家类型时触发
    def change_player_b(self):
        # 非账号用户时，账号栏和密码栏无效
        player_b = self.Box_b.currentIndex()
        if player_b == USER:
            self.act_Input_b.setText("")
            self.pwd_Input_b.setText("")
            self.act_Input_b.setStyleSheet("color: black;")
            self.pwd_Input_b.setStyleSheet("color: black;")
            self.act_Input_b.setReadOnly(False)
            self.pwd_Input_b.setReadOnly(False)
        else:
            self.act_Input_b.setText("非账号用户无需输入")
            self.pwd_Input_b.setText("非账号用户无需输入")
            self.act_Input_b.setStyleSheet("color: lightgray;")
            self.pwd_Input_b.setStyleSheet("color: lightgray;")
            self.act_Input_b.setReadOnly(True)
            self.pwd_Input_b.setReadOnly(True)



    # 改变白棋玩家类型时触发
    def change_player_w(self):
        # 非账号用户时，账号栏和密码栏无效
        player_w = self.Box_w.currentIndex()
        if player_w == USER:
            self.act_Input_w.setText("")
            self.pwd_Input_w.setText("")
            self.act_Input_w.setStyleSheet("color: black;")
            self.pwd_Input_w.setStyleSheet("color: black;")
            self.act_Input_w.setReadOnly(False)
            self.pwd_Input_w.setReadOnly(False)
        else:
            self.act_Input_w.setText("非账号用户无需输入")
            self.pwd_Input_w.setText("非账号用户无需输入")
            self.act_Input_w.setStyleSheet("color: lightgray;")
            self.pwd_Input_w.setStyleSheet("color: lightgray;")
            self.act_Input_w.setReadOnly(True)
            self.pwd_Input_w.setReadOnly(True)




    # 点击“登录黑棋账号”触发
    def login_b(self):
        # 如果是账号用户，那么需要检测账号
        player_b = self.Box_b.currentIndex()
        if player_b == USER:
            # 检测是否检测输入了黑棋账号
            act_b = self.act_Input_b.text()
            if act_b == "":
                QMessageBox.information(self, "提示", "请输入黑棋账号！")
                return
            # 检测输入的act_b是否有5位
            act_b_n = int(act_b)
            if act_b_n < 10000:
                QMessageBox.information(self, "提示", "黑棋账号长度不足5位！")
                return
            # 检测是否检测输入了黑棋密码
            pwd_b = self.pwd_Input_b.text()
            if pwd_b == "":
                QMessageBox.information(self, "提示", "请输入黑棋密码！")
                return

            # 接下来读取用户数据，并判断密码是否正确
            base_directory = os.path.abspath(os.path.join(os.getcwd(), "../usr_data"))  # 用户数据目录
            folder_path = os.path.join(base_directory, act_b)  # 以账号为名字的文件夹路径
            # 判断用户是否存在（文件夹是否存在）
            if os.path.exists(folder_path) == False:
                QMessageBox.information(self, "提示", f"账号 '{act_b}' 不存在！")
                return
            file_path = os.path.join(folder_path, "info.txt")  # 用户信息文件
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    lines = file.readlines()
                # 逐行解析文件内容
                for i, line in enumerate(lines):
                    line = line.strip()
                    if line.startswith("username:"):
                        self.username_b = line.split(": ")[1].strip()
                    elif line.startswith("account:"):
                        self.act_b = line.split(": ")[1].strip()
                    elif line.startswith("password:"):
                        self.pwd_b = line.split(": ")[1].strip()
                    elif line.startswith("AllPlays:"):
                        self.AllPlays_b = line.split(": ")[1].strip()
                    elif line.startswith("WinPlays:"):
                        self.WinPlays_b = line.split(": ")[1].strip()
            except Exception as e:
                print(f"打开文件失败: {e}")
                return
            # 判断密码是否正确
            if pwd_b != self.pwd_b:
                QMessageBox.information(self, "提示", f"密码不正确！")
                return

        # 由黑棋的登陆界面切换成黑棋选手的信息界面
        self.widget_b1.setGeometry(QtCore.QRect(50, 50, 0, 0))
        self.widget_b2.setGeometry(QtCore.QRect(50, 50, 251, 211))
        # 黑棋登录成功
        self.login_status_b = True
        self.player_b = player_b
        # 黑棋玩家的类型
        self.player_label_b.setText(self.Box_b.currentText())
        # 若是账号用户则显示账号、用户名、总场次和胜场
        if self.player_b == USER:
            self.act_label_b2.setText(self.act_b)
            self.name_label_b2.setText(self.username_b)
            self.all_label_b2.setText(self.AllPlays_b)
            self.win_label_b2.setText(self.WinPlays_b)
        # 若非账号用户则不显示账号、用户名、总场次和胜场
        else:
            self.act_label_b2.setText('无')
            self.name_label_b2.setText('无')
            self.all_label_b2.setText('无')
            self.win_label_b2.setText('无')




    # 点击“登录白棋账号”触发
    def login_w(self):
        # 如果是账号用户，那么需要检测账号
        player_w = self.Box_w.currentIndex()
        if player_w == USER:
            # 检测是否检测输入了白棋账号
            act_w = self.act_Input_w.text()
            if act_w == "":
                QMessageBox.information(self, "提示", "请输入白棋账号！")
                return
            # 检测输入的act_w是否有5位
            act_w_n = int(act_w)
            if act_w_n < 10000:
                QMessageBox.information(self, "提示", "白棋账号长度不足5位！")
                return
            # 检测是否检测输入了白棋密码
            pwd_w = self.pwd_Input_w.text()
            if pwd_w == "":
                QMessageBox.information(self, "提示", "请输入白棋密码！")
                return

            # 接下来读取用户数据，并判断密码是否正确
            base_directory = os.path.abspath(os.path.join(os.getcwd(), "../usr_data"))  # 用户数据目录
            folder_path = os.path.join(base_directory, act_w)                           # 以账号为名字的文件夹路径
            # 判断用户是否存在（文件夹是否存在）
            if os.path.exists(folder_path) == False:
                QMessageBox.information(self, "提示", f"账号 '{act_w}' 不存在！")
                return
            file_path = os.path.join(folder_path, "info.txt")   # 用户信息文件
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    lines = file.readlines()
                # 逐行解析文件内容
                for i, line in enumerate(lines):
                    line = line.strip()
                    if line.startswith("username:"):
                        self.username_w = line.split(": ")[1].strip()
                    elif line.startswith("account:"):
                        self.act_w = line.split(": ")[1].strip()
                    elif line.startswith("password:"):
                        self.pwd_w = line.split(": ")[1].strip()
                    elif line.startswith("AllPlays:"):
                        self.AllPlays_w = line.split(": ")[1].strip()
                    elif line.startswith("WinPlays:"):
                        self.WinPlays_w = line.split(": ")[1].strip()
            except Exception as e:
                print(f"打开文件失败: {e}")
                return
            # 判断密码是否正确
            if pwd_w != self.pwd_w:
                QMessageBox.information(self, "提示", f"密码不正确！")
                return


        # 由白棋的登陆界面切换成白棋选手的信息界面
        self.widget_w1.setGeometry(QtCore.QRect(380, 50, 0, 0))
        self.widget_w2.setGeometry(QtCore.QRect(380, 50, 251, 211))
        # 白棋登录成功
        self.login_status_w = True
        self.player_w = player_w
        # 白棋玩家的类型
        self.player_label_w.setText(self.Box_w.currentText())
        # 若是账号用户则显示账号、用户名、总场次和胜场
        if self.player_w == USER:
            self.act_label_w2.setText(self.act_w)
            self.name_label_w2.setText(self.username_w)
            self.all_label_w2.setText(self.AllPlays_w)
            self.win_label_w2.setText(self.WinPlays_w)
        # 若非账号用户则不显示账号、用户名、总场次和胜场
        else:
            self.act_label_w2.setText('无')
            self.name_label_w2.setText('无')
            self.all_label_w2.setText('无')
            self.win_label_w2.setText('无')




    # 点击“退出黑棋账号”触发
    def logout_b(self):
        # 由黑棋选手的信息界面切换成黑棋的登陆界面
        self.widget_b1.setGeometry(QtCore.QRect(50, 50, 251, 211))
        self.widget_b2.setGeometry(QtCore.QRect(50, 50, 0, 0))
        self.login_status_b = False



    # 点击“退出白棋账号”触发
    def logout_w(self):
        # 由白棋选手的信息界面切换成白棋的登陆界面
        self.widget_w1.setGeometry(QtCore.QRect(380, 50, 251, 211))
        self.widget_w2.setGeometry(QtCore.QRect(380, 50, 0, 0))
        self.login_status_w = False



    # 点击“注册账号”触发
    def register(self):
        self.win_ctrl.switch_win(LOGIN_2_REGISTER)



    # 点击“开始游戏”触发
    def start_game(self):
        # 判断两个棋手是否都登录了
        if self.login_status_w != True or self.login_status_b != True:
            QMessageBox.information(self, "提示", f"有棋手未登录！")
            return

        # 设置两个棋手选择的玩家状态：账号用户/游客/一级AI/二级AI
        self.win_ctrl.set_player(self.player_w, self.player_b)
        # 设置黑棋的用户名、账号、总场次、胜场
        if self.player_b == USER:
            self.win_ctrl.set_player_b_info(self.username_b, self.act_b, self.AllPlays_b, self.WinPlays_b)
        # 设置白棋的用户名、账号、总场次、胜场
        if self.player_w == USER:
            self.win_ctrl.set_player_w_info(self.username_w, self.act_w, self.AllPlays_w, self.WinPlays_w)

        # 切换至开始窗口
        self.win_ctrl.switch_win(LOGIN_2_START)

