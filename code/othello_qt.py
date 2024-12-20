# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'othello_ui.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_OthelloWindow(object):
    def setupUi(self, OthelloWindow):
        OthelloWindow.setObjectName("OthelloWindow")
        OthelloWindow.resize(871, 577)
        OthelloWindow.setMaximumSize(QtCore.QSize(1300, 1000))
        OthelloWindow.setStyleSheet("")
        OthelloWindow.setAnimated(True)
        self.centralwidget = QtWidgets.QWidget(OthelloWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.ChessCan = QtWidgets.QWidget(self.centralwidget)
        self.ChessCan.setGeometry(QtCore.QRect(630, 350, 220, 220))
        self.ChessCan.setStyleSheet("border-image: url(:/bg/image/blacks-removebg-preview.png);")
        self.ChessCan.setObjectName("ChessCan")
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(610, 90, 251, 251))
        self.textBrowser.setStyleSheet("background-color: rgba(255, 255, 255, 150);")
        self.textBrowser.setObjectName("textBrowser")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(700, 100, 81, 20))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(620, 130, 111, 18))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(620, 160, 161, 18))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.result_label = QtWidgets.QLabel(self.centralwidget)
        self.result_label.setGeometry(QtCore.QRect(40, 80, 521, 191))
        font = QtGui.QFont()
        font.setPointSize(90)
        self.result_label.setFont(font)
        self.result_label.setText("")
        self.result_label.setObjectName("result_label")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(620, 190, 251, 20))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.textBrowser_2 = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser_2.setGeometry(QtCore.QRect(610, 0, 251, 91))
        self.textBrowser_2.setStyleSheet("background-color: rgba(255, 255, 255, 150);")
        self.textBrowser_2.setObjectName("textBrowser_2")
        self.yeildBtn = QtWidgets.QPushButton(self.centralwidget)
        self.yeildBtn.setGeometry(QtCore.QRect(620, 50, 71, 28))
        self.yeildBtn.setObjectName("yeildBtn")
        self.restartBtn = QtWidgets.QPushButton(self.centralwidget)
        self.restartBtn.setGeometry(QtCore.QRect(700, 50, 71, 28))
        self.restartBtn.setObjectName("restartBtn")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(680, 10, 111, 20))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.chessboardno = QtWidgets.QWidget(self.centralwidget)
        self.chessboardno.setGeometry(QtCore.QRect(0, -10, 601, 601))
        self.chessboardno.setStyleSheet("border-image: url(:/bg/image/chessboard1.png);")
        self.chessboardno.setObjectName("chessboardno")
        self.chessboard = QtWidgets.QLabel(self.centralwidget)
        self.chessboard.setGeometry(QtCore.QRect(0, -10, 601, 601))
        font = QtGui.QFont()
        font.setPointSize(90)
        self.chessboard.setFont(font)
        self.chessboard.setText("")
        self.chessboard.setObjectName("chessboard")
        self.recordBtn = QtWidgets.QPushButton(self.centralwidget)
        self.recordBtn.setGeometry(QtCore.QRect(780, 50, 71, 28))
        self.recordBtn.setObjectName("recordBtn")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(660, 220, 211, 20))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(660, 250, 211, 20))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.label_9 = QtWidgets.QLabel(self.centralwidget)
        self.label_9.setGeometry(QtCore.QRect(660, 280, 211, 20))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_9.setFont(font)
        self.label_9.setObjectName("label_9")
        self.label_10 = QtWidgets.QLabel(self.centralwidget)
        self.label_10.setGeometry(QtCore.QRect(660, 310, 211, 20))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_10.setFont(font)
        self.label_10.setObjectName("label_10")
        OthelloWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(OthelloWindow)
        QtCore.QMetaObject.connectSlotsByName(OthelloWindow)

    def retranslateUi(self, OthelloWindow):
        _translate = QtCore.QCoreApplication.translate
        OthelloWindow.setWindowTitle(_translate("OthelloWindow", "MainWindow"))
        self.textBrowser.setHtml(_translate("OthelloWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'SimSun\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:10.8pt;\"><br /></p></body></html>"))
        self.label.setText(_translate("OthelloWindow", "玩家信息"))
        self.label_2.setText(_translate("OthelloWindow", "步数：0"))
        self.label_3.setText(_translate("OthelloWindow", "时间：00:00"))
        self.label_4.setText(_translate("OthelloWindow", "当前棋手：黑棋"))
        self.textBrowser_2.setHtml(_translate("OthelloWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'SimSun\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:10.8pt;\"><br /></p></body></html>"))
        self.yeildBtn.setText(_translate("OthelloWindow", "认输"))
        self.restartBtn.setText(_translate("OthelloWindow", "重新开始"))
        self.label_5.setText(_translate("OthelloWindow", "用户可选操作"))
        self.recordBtn.setText(_translate("OthelloWindow", "保存录像"))
        self.label_6.setText(_translate("OthelloWindow", "账号：  无"))
        self.label_7.setText(_translate("OthelloWindow", "用户名：无"))
        self.label_9.setText(_translate("OthelloWindow", "总场次：0"))
        self.label_10.setText(_translate("OthelloWindow", "胜场：  0"))
import chess_qrc_rc
