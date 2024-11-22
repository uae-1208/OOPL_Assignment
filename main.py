# -*- coding: utf-8 -*-

import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel
from MACRO import *
from timer import GameTime
from ui import Ui_MainWindow



# 重新定义Label类
class LaBel(QLabel):
    def __init__(self, parent):
        super().__init__(parent)
        self.setMouseTracking(True)

    def enterEvent(self, e):
        e.ignore()



class MyMainForm(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MyMainForm, self).__init__(parent)
        self.setupUi(self)

        # 鼠标相关
        self.setCursor(Qt.PointingHandCursor)                   # 鼠标变成手指形状
        self.BlackPic = QPixmap('./designer/image/black.png')   # 黑棋图片
        self.WhitePic = QPixmap('./designer/image/white.png')   # 白棋图片
        self.mouse_point = LaBel(self)                          # 将鼠标图片改为棋子
        self.mouse_point.setScaledContents(True)                # 图片大小根据标签大小可变
        self.mouse_point.setGeometry(1100, 750, 64, 64) # 设置图片大小和坐标
        self.setMouseTracking(True)                             # 鼠标不按下时的移动也能捕捉到
        self.mouse_point.raise_()                               # 鼠标始终在最上层

        # 系统状态
        self.status = BLACK_PLAY                    # 棋局状态，黑棋先行
        self.mouse_point.setPixmap(self.BlackPic)   # 加载黑棋
        self.step = 0                               # 步数
        self.size = 15                              # 棋盘大小

        # 计时器timer
        self.game_time = GameTime(self.label_3)
        self.game_time._signal.connect(self.set_time)
        self.game_time.set_status(1)
        self.game_time.start()

        # 棋盘：一行有self.size个chess，一共有self.size行
        self.chessboard = []
        for row in range(self.size):        # 行循环
            chess_row = []  # 一行chess
            for col in range(self.size):    # 列循环
                # 每一个chess由{UI中的坐标}、{落子状态}和{一个LaBel对象}构成
                chess_temp = {'coord': {'x': 40+64*row, 'y': 40+64*col}, 'chess': IDLE, 'label':LaBel(self)}
                chess_temp['label'].setVisible(True)        # 图片可视
                chess_temp['label'].setScaledContents(True) # 图片大小根据标签大小可变
                chess_row.append(chess_temp)
            self.chessboard.append(chess_row)



    # timer的槽函数：让label显示当前时间，实时更新
    def set_time(self,time):
        self.label_3.setText("时间：{}".format(time))



    # 鼠标移动event
    def mouseMoveEvent(self, e):
        self.mouse_point.move(e.x() - 32 , e.y() - 32)  # 棋子随鼠标移动



    # 鼠标点击event：玩家下棋
    def mousePressEvent(self, e):
        # 若对局结束，则退出
        if self.status == END:
            return

        # 按下了左键
        if e.button() == Qt.LeftButton:
            # 检查落在位置是否在棋盘内，棋盘范围（40，40）~（960，960）
            if e.x() >= 40 and e.x() <= 960 and e.y() >= 40 and e.y() <= 960:
                # 获取鼠标点击位置所对应的chess在UI界面中的坐标，以及chessboard中的坐标
                chess_uix, chess_uiy, chess_x,chess_y = self.get_coord(e.x(), e.y())

                # 如果未能确定棋子精确位置(x == -1)，或者该位置已有棋子(a!=0)，就不允许落子
                if chess_uix == -1 or self.chessboard[chess_x][chess_y]['chess'] != IDLE:
                    return

                # 棋局更新
                self.update(chess_uix-16, chess_uiy-16, chess_x, chess_y)    # 减16是为了保证棋子处于棋盘十字线中心位置

                #判断输赢,根据结果决定是否继续棋局
                self.judge(chess_x, chess_y)

                # 切换棋手
                self.switch_status()



    # 判断每次落子在米字方向上是否有五个连续的棋子
    def judge(self,chess_x,chess_y):
        dir = [(-1,0),(1,0),(-1,1),(1,-1),(0,1),(0,-1),(1,1),(-1,-1)]    # 8个方向
        i = 0
        while i < len(dir):
            count = 1   # 算上本身的chess
            #循环两次，分别判断两个相对的方向
            for a in range(2):
                x, y = chess_x, chess_y
                for j in range(4):
                    x += dir[i][0]
                    y += dir[i][1]
                    # 若当chess超出界限，中止该方向的判断
                    if x<0 or x>self.size-1 or y<0 or y>self.size-1:
                        break
                    # 若当前方向上出现另一颜色棋子，中止该方向的判断
                    if self.chessboard[x][y]['chess'] == self.chessboard[chess_x][chess_y]['chess']:
                        count += 1
                    else:
                        break
                i += 1

            if count >= 5:
                self.game_time.set_status(0)            # 计时停止
                self.status = END                       # 终止棋局
                result_label = LaBel(self)              # 结果标签
                result_label.setVisible(True)           # 图片可视
                result_label.setScaledContents(True)    # 图片大小根据标签大小可变

                if self.chessboard[chess_x][chess_y]['chess'] == BLACK:
                    print("黑子胜出")
                    pic = QPixmap('./designer/image/black_win.jpg')
                else:
                    print("白子胜出")
                    pic = QPixmap('./designer/image/white_win.jpg')
                result_label.setPixmap(pic)
                result_label.setGeometry(203, 393, 554, 174)
                return 0    # 结束棋局

        return 1    #继续棋局



    # 遍历所有chess
    # 获取鼠标点击位置所对应的chess在UI界面中的坐标，以及chessboard中的坐标
    def get_coord(self,m_x,m_y):
        for row in range(self.size):
            for col in range(self.size):
                chess_temp = self.chessboard[row][col]
                dist = self.distance(m_x, m_y, chess_temp['coord']['x'], chess_temp['coord']['y'])

                # 与棋盘点的距离不超过32
                if dist <= 32:
                    return chess_temp['coord']['x'], chess_temp['coord']['y'], row, col

        return -1,-1,-1,-1  #默认返回



    #求两点距离
    def distance(self,x1,y1,x2,y2):
        return ((x1-x2)**2 + (y1-y2)**2)**0.5



    # 棋局更新
    def update(self,chess_uix,chess_uiy,chess_x,chess_y):
        # 显示刚下的棋子
        if self.status == BLACK_PLAY:
            self.chessboard[chess_x][chess_y]['label'].setPixmap(self.BlackPic)  # 放置黑色棋子
        elif self.status == WHITE_PLAY:
            self.chessboard[chess_x][chess_y]['label'].setPixmap(self.WhitePic)  # 放置白色棋子
        self.chessboard[chess_x][chess_y]['label'].setGeometry(chess_uix, chess_uiy, 64, 64) # 设置位置，大小


        self.chessboard[chess_x][chess_y]['chess'] = self.status
        self.step += 1
        self.label_2.setText("步数：{}".format(self.step))


    # 切换棋手状态
    def switch_status(self):
        if self.status == BLACK_PLAY:
            self.mouse_point.setPixmap(self.WhitePic)  # 加载白棋
            # uae:label_4
            self.label_7.setText("当前棋手：白棋")
            # uae:self.chess
            self.black.setStyleSheet("background-image: url(:/bg/image/whites-removebg-preview.png);\n"
                                      "background-color: rgba(255, 255, 255, 0);")
            self.status = WHITE_PLAY
        elif self.status == WHITE_PLAY:
            self.mouse_point.setPixmap(self.BlackPic)  # 加载黑棋
            # uae:label_4
            self.label_7.setText("当前棋手：黑棋")
            # uae:self.chess
            self.black.setStyleSheet("background-image: url(:/bg/image/blacks-removebg-preview.png);\n"
                                      "background-color: rgba(255, 255, 255, 0);")
            self.status = BLACK_PLAY



if __name__ == "__main__":
    # 固定的，PyQt5程序都需要QApplication对象。sys.argv是命令行参数列表，确保程序可以双击运行
    app = QApplication(sys.argv)
    # 初始化
    myWin = MyMainForm()
    #设置标题图标
    myWin.setWindowIcon(QIcon('./favicon.ico'))
    #设置标题
    myWin.setWindowTitle('五子棋双人对战')
    # 将窗口控件显示在屏幕上
    myWin.show()
    # 程序运行，sys.exit方法确保程序完整退出。
    sys.exit(app.exec_())