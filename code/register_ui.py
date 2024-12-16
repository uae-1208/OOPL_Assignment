import os
import random
from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5.QtGui import QIcon, QIntValidator
from MACRO import *
from register_qt import Ui_StartWindow



class RegisterUI(QMainWindow, Ui_StartWindow):
    def __init__(self, parent=None, wc=None):
        super(RegisterUI, self).__init__(parent)
        self.setupUi(self)
        self.win_ctrl = wc

        # 设置账号Input的验证器：账号必须是5位的数字
        int_validator = QIntValidator(0, 99999, self)
        # 账号必须是5位的数字，后续还要判断是否大于等于10000
        self.act_input.setValidator(int_validator)
        # 密码必须是不超过5位的数字
        self.pwd_Input.setValidator(int_validator)
        # 点击“注册”
        self.register_btn.clicked.connect(self.register)
        # 点击“返回登陆”
        self.return_btn.clicked.connect(self.rtn)


    # 点击“注册”时触发
    def register(self):
        # 检测是否检测输入了用户名
        username = self.name_input.text()
        if username == "":
            QMessageBox.information(self, "提示", "请输入用户名号！")
            return

        # 检测是否检测输入了账号
        act = self.act_input.text()
        if act == "":
            QMessageBox.information(self, "提示", "请输入账号！")
            return
        # 检测输入的act是否有5位
        act_n = int(act)
        if act_n < 10000:
            QMessageBox.information(self, "提示", "账号长度不足5位！")
            return

        # 检测是否检测输入了密码
        pwd = self.pwd_Input.text()
        if pwd == "":
            QMessageBox.information(self, "提示", "请输入密码！")
            return

        # 定义存储目录（../usr_data），并以用户名为名字创建文件夹路径
        base_directory = os.path.abspath(os.path.join(os.getcwd(), "../usr_data"))
        folder_path = os.path.join(base_directory, act)
        # 判断用户是否已存在（文件夹是否存在）
        if os.path.exists(folder_path):
            QMessageBox.information(self, "提示", f"账号 '{act}' 已存在！")
            return
        #创建文件夹
        try:
            os.makedirs(folder_path, exist_ok=True) # 确保 ../usr_data 目录存在
        except Exception as e:
            print(f"创建文件夹失败: {e}")
            return
        # 在该文件夹中创建一个 txt 文件，写入用户信息
        file_path = os.path.join(folder_path, "info.txt")
        try:
            random_number1 = random.randint(51, 100)
            random_number2 = random.randint(0, 50)
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(f"username: {username}\n")
                file.write(f"account: {act}\n")
                file.write(f"password: {pwd}\n")
                file.write(f"AllPlays: {random_number1}\n")
                file.write(f"WinPlays: {random_number2}\n")
        except Exception as e:
            print(f"写入文件失败: {e}")
            return

        QMessageBox.information(self, "提示", "注册成功！")



    # 点击“返回登陆”时触发
    def rtn(self):
        self.win_ctrl.switch_win(REGISTER_2_LOGIN)


    # 重写 closeEvent，当用户点击关闭按钮时自动返回到登录界面
    def closeEvent(self, event):
        self.win_ctrl.switch_win(REGISTER_2_LOGIN)

