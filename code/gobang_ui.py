from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow, QLabel, QFileDialog, QMessageBox
from MACRO import *
from timer import GameTime
from gobang_qt import Ui_GobangWindow


# 重新定义Label类
class LaBel(QLabel):
    def __init__(self, parent):
        super().__init__(parent)
        self.setMouseTracking(True)

    def enterEvent(self, e):
        e.ignore()



# 五子棋UI
class GobangUI(QMainWindow, Ui_GobangWindow):
    def __init__(self, parent=None, wc=None):
        super(GobangUI, self).__init__(parent)
        self.setupUi(self)
        self.win_ctrl = wc

        # 鼠标相关
        self.setCursor(Qt.PointingHandCursor)                   # 鼠标变成手指形状
        self.BlackPic = QPixmap('../designer/image/black.png')  # 黑棋图片
        self.WhitePic = QPixmap('../designer/image/white.png')  # 白棋图片
        self.mouse_point = LaBel(self)                          # 将鼠标图片改为棋子
        self.mouse_point.setScaledContents(True)                # 图片大小根据标签大小可变
        self.mouse_point.setGeometry(1100, 650, 64, 64)  # 设置图片大小和坐标
        self.setMouseTracking(True)                             # 鼠标不按下时的移动也能捕捉到
        self.mouse_point.raise_()                               # 鼠标始终在最上层

        # 系统状态
        self.status = BLACK_PLAY                    # 棋局状态，黑棋先行
        self.mouse_point.setPixmap(self.BlackPic)   # 加载黑棋
        self.retract_lock = UNLOCKED                # 是否可以悔棋
        self.step = 0                               # 步数
        self.size = 15                              # 棋盘大小
        self.last_step = {}                         # 保留上一步走棋情况

        # 按钮类
        self.yeildBtn.clicked.connect(self.yeild)           # 投降
        self.retractBtn.clicked.connect(self.retractAstep)  # 悔棋一步
        self.restartBtn.clicked.connect(self.restart)       # 重新开始
        self.storeBtn.clicked.connect(self.save_chess)      # 保存棋局
        self.loadBtn.clicked.connect(self.load_chess)       # 导入棋局

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



    # 鼠标移动event，移动鼠标时会触发
    def mouseMoveEvent(self, e):
        # 如果鼠标在棋盘范围内，则显示棋子图片
        if e.x() >= 0 and e.x() <= 960 and e.y() >= 0 and e.y() <= 960:
            self.mouse_point.move(e.x() - 32 , e.y() - 32)  # 棋子随鼠标移动
            self.mouse_point.show()
        # 否则隐藏棋子图片
        else:
            self.mouse_point.hide()



    # 鼠标点击event：玩家下棋。点击鼠标时会触发
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
                    QMessageBox.information(self, "提示", "当前位置已有落子！")
                    return
                # 棋局更新
                self.update(chess_uix-20, chess_uiy-20, chess_x, chess_y)    # 减20是为了保证棋子处于棋盘十字线中心位置
                #判断输赢,根据结果决定是否继续棋局
                if self.judge(chess_x, chess_y):
                    return
                # 切换棋手
                self.switch_status()
                # 保存这一步走棋
                self.last_step['chess_x'] = chess_x
                self.last_step['chess_y'] = chess_y



    # 判断每次落子在米字方向上是否有五个连续的棋子。由mousePressEvent调用
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

            # 棋手胜出
            if count >= 5:
                self.end_game(self.status)
                return 1    # 有棋手胜出

        return 0    # 无棋手胜出



    # 终结棋局。由judge、yeild调用
    def end_game(self, winner):
        self.game_time.set_status(0)                # 计时停止
        self.status = END                           # 终止棋局
        self.result_label = LaBel(self)             # 结果标签
        self.result_label.setVisible(True)          # 图片可视
        self.result_label.setScaledContents(True)  # 图片大小根据标签大小可变

        if winner == BLACK_PLAY:
            print("黑子胜出")
            pic = QPixmap('../designer/image/black_win.jpg')
        else:
            print("白子胜出")
            pic = QPixmap('../designer/image/white_win.jpg')
        self. result_label.setPixmap(pic)
        self.result_label.setGeometry(203, 393, 554, 174)



    # 认输。点击“投降”时调用
    def yeild(self):
        if self.status == END:
            QMessageBox.information(self, "提示", "棋局已结束，您无法认输！")
            return

        self.end_game(WHITE_PLAY if self.status == BLACK_PLAY else BLACK_PLAY)



    # 重新开始。点击“重新开始”时调用
    def restart(self):
        self.close()



    # 悔棋。点击“悔棋”时调用
    def retractAstep(self):
        # 刚开局或者棋局结束或者当前棋手悔棋一次时，无法再悔棋
        if self.step == 0:
            QMessageBox.information(self, "提示", "棋局刚开始，您无法悔棋！")
            return
        if self.status == END:
            QMessageBox.information(self, "提示", "棋局已结束，您无法悔棋！")
            return
        if self.retract_lock == LOCKED:
            QMessageBox.information(self, "提示", "您的悔棋次数已经用完了！")
            return

        # 回退步数
        self.step -= 1
        self.label_2.setText("步数：{}".format(self.step))
        # 去掉棋子
        self.chessboard[self.last_step['chess_x']][self.last_step['chess_y']]['label'].hide()
        self.chessboard[self.last_step['chess_x']][self.last_step['chess_y']]['chess'] = IDLE
        # 切换棋手
        self.switch_status()
        # 限制棋手再次悔棋
        self.retract_lock = LOCKED



    # 保存棋局。点击“保存棋局”时调用
    def save_chess(self):
        # 棋局结束时，无法再保存棋局
        if self.status == END:
            QMessageBox.information(self, "提示", "棋局已结束，您无法保存棋局！")
            return

        # 第一个参数必须是None，否则程序会崩
        destpath, filetype = QFileDialog.getSaveFileName(None, "文件保存", "chess.txt", "文本 (*.txt)")

        # 将棋局的信息保存到文件中
        if destpath:
            with open(destpath, "w", encoding="utf-8") as file:
                file.write("size: "f"{self.size}x{self.size}\n")
                file.write("step: "f"{self.step}\n")
                file.write("status: "f"{self.status}\n")
                file.write("retract_lock: "f"{self.retract_lock}\n")
                file.write("last_step: " f"{self.last_step['chess_x']} {self.last_step['chess_y']}\n")
                file.write("chess: \n")
                # 需要注意，保存的txt分布与实际的棋局是中心对称的
                for row in range(self.size):  # 行循环
                    for col in range(self.size):  # 列循环
                        file.write(f"{self.chessboard[row][col]['chess']} ")
                    file.write("\n")
        else:  # 用户点击取消后的处理，否则程序会出错退出
            QMessageBox.information(self, "提示", "由于未选择保存位置，文件保存操作已取消！")



    # 导入棋局。点击“导入棋局”时调用
    def load_chess(self):
        # 棋局结束时，无法再导入棋局
        if self.status == END:
            QMessageBox.information(self, "提示", "棋局已结束，您无法导入棋局！")
            return

        # 第一个参数必须是None，否则程序会崩
        srcpath, type = QFileDialog.getOpenFileName(None, "文件保存", "chess.txt", "文本 (*.txt)")

        if srcpath: # 判断文件是否被打开
            # 逐读取文件
            with open(srcpath, "r", encoding="utf-8") as file:
                lines = file.readlines()

            # 逐行解析文件内容
            for i, line in enumerate(lines):
                line = line.strip()
                if line.startswith("size:"):
                    size_str = line.split(": ")[1].strip()
                    self.size = int(size_str.split("x")[0])  # 提取第一个数字
                elif line.startswith("step:"):
                    self.step = int(line.split(": ")[1].strip())
                elif line.startswith("status:"):
                    self.status = int(line.split(": ")[1].strip())
                elif line.startswith("retract_lock:"):
                    self.retract_lock = int(line.split(": ")[1].strip())
                elif line.startswith("last_step:"):
                    last_step_str = line.split(": ")[1].strip()
                    x, y = map(int, last_step_str.split())
                    self.last_step["chess_x"] = x
                    self.last_step["chess_y"] = y
                elif line.startswith("chess:"):
                    # 开始读取棋盘部分
                    chessboard_temp = []
                    for row_line in lines[i+1: i+1+self.size]:  # 按行读取棋盘数据
                        row = list(map(int, row_line.split()))
                        chessboard_temp.append(row)

            # 恢复系统数据
            # 步数
            self.label_2.setText("步数：{}".format(self.step))
            # 棋手
            if self.status == WHITE_PLAY:
                self.mouse_point.setPixmap(self.WhitePic)  # 加载白棋
                self.label_4.setText("当前棋手：白棋")
                self.ChessCan.setStyleSheet("background-image: url(:/bg/image/whites-removebg-preview.png);\n"
                                            "background-color: rgba(255, 255, 255, 0);")
            elif self.status == BLACK_PLAY:
                self.mouse_point.setPixmap(self.BlackPic)  # 加载黑棋
                self.label_4.setText("当前棋手：黑棋")
                self.ChessCan.setStyleSheet("background-image: url(:/bg/image/blacks-removebg-preview.png);\n"
                                            "background-color: rgba(255, 255, 255, 0);")
            # 棋局
            for row in range(self.size):  # 行循环
                for col in range(self.size):  # 列循环
                    chess = chessboard_temp[row][col]
                    self.chessboard[row][col]['chess'] = chess
                    if chess == BLACK:
                        self.chessboard[row][col]['label'].setPixmap(self.BlackPic)  # 放置黑色棋子
                        self.chessboard[row][col]['label'].setGeometry(40+64*row-20, 40+64*col-20, 64, 64)  # 设置位置，大小
                        self.chessboard[row][col]['label'].show()
                    elif chess == WHITE:
                        self.chessboard[row][col]['label'].setPixmap(self.WhitePic)  # 放置白色棋子
                        self.chessboard[row][col]['label'].setGeometry(40+64*row-20, 40+64*col-20, 64, 64)  # 设置位置，大小
                        self.chessboard[row][col]['label'].show()
                    elif chess == IDLE:
                        self.chessboard[row][col]['label'].hide()

        else:  # 用户点击取消后的处理，否则程序会出错退出
            QMessageBox.information(self, "提示", "由于未选择导入位置，文件导入操作已取消！")




    # 获取鼠标点击位置所对应的chess在UI界面中的坐标，以及chessboard中的坐标。由mousePressEvent调用。
    def get_coord(self,m_x,m_y):
        # 遍历所有chess
        for row in range(self.size):
            for col in range(self.size):
                chess_temp = self.chessboard[row][col]
                dist = self.distance(m_x, m_y, chess_temp['coord']['x'], chess_temp['coord']['y'])

                # 与棋盘点的距离不超过32
                if dist <= 32:
                    return chess_temp['coord']['x'], chess_temp['coord']['y'], row, col

        return -1,-1,-1,-1  #默认返回



    #求两点距离。由get_coord调用。
    def distance(self,x1,y1,x2,y2):
        return ((x1-x2)**2 + (y1-y2)**2)**0.5



    # 棋局更新。由mousePressEvent调用。
    def update(self,chess_uix,chess_uiy,chess_x,chess_y):
        # 显示刚下的棋子
        if self.status == BLACK_PLAY:
            self.chessboard[chess_x][chess_y]['label'].setPixmap(self.BlackPic)  # 放置黑色棋子
        elif self.status == WHITE_PLAY:
            self.chessboard[chess_x][chess_y]['label'].setPixmap(self.WhitePic)  # 放置白色棋子
        self.chessboard[chess_x][chess_y]['label'].setGeometry(chess_uix, chess_uiy, 64, 64) # 设置位置，大小
        self.chessboard[chess_x][chess_y]['label'].show()

        self.chessboard[chess_x][chess_y]['chess'] = self.status
        self.step += 1
        self.label_2.setText("步数：{}".format(self.step))



    # 切换棋手状态。由mousePressEven或者retractAstep调用。
    def switch_status(self):
        # 切换棋手，悔棋次数恢复
        self.retract_lock = UNLOCKED

        if self.status == BLACK_PLAY:
            self.mouse_point.setPixmap(self.WhitePic)  # 加载白棋
            self.label_4.setText("当前棋手：白棋")
            self.ChessCan.setStyleSheet("background-image: url(:/bg/image/whites-removebg-preview.png);\n"
                                        "background-color: rgba(255, 255, 255, 0);")
            self.status = WHITE_PLAY
        elif self.status == WHITE_PLAY:
            self.mouse_point.setPixmap(self.BlackPic)  # 加载黑棋
            self.label_4.setText("当前棋手：黑棋")
            self.ChessCan.setStyleSheet("background-image: url(:/bg/image/blacks-removebg-preview.png);\n"
                                        "background-color: rgba(255, 255, 255, 0);")
            self.status = BLACK_PLAY



    # 重写 closeEvent，当用户点击关闭按钮时自动返回开始录界面
    def closeEvent(self, event):
        self.win_ctrl.switch_win(GOBANG_2_START)

