import MCTS as rvs
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QKeyEvent
from PyQt5.QtWidgets import QMainWindow, QLabel, QFileDialog, QMessageBox
from MACRO import *
from timer import GameTime
from othello_qt import Ui_OthelloWindow
from MCTS import *


# 重新定义Label类
class LaBel(QLabel):
    def __init__(self, parent):
        super().__init__(parent)
        self.setMouseTracking(True)

    def enterEvent(self, e):
        e.ignore()



# 黑白棋UI
class OthelloUI(QMainWindow, Ui_OthelloWindow):
    def __init__(self, parent=None, wc=None):
        super(OthelloUI, self).__init__(parent)
        self.setupUi(self)
        self.win_ctrl = wc

        # 显示棋盘
        self.chessboard.setPixmap(QPixmap('../designer/image/chessboard1.png'))

        # 棋手信息相关
        self.player_w, self.player_b = self.win_ctrl.get_player()
        # 返回黑棋的用户名、账号、总场次、胜场
        if self.player_b == USER:
            self.username_b, self.act_b, self.AllPlays_b, self.WinPlays_b = self.win_ctrl.get_player_b_info()
        # 返回白棋的用户名、账号、总场次、胜场
        if self.player_w == USER:
            self.username_w, self.act_w, self.AllPlays_w, self.WinPlays_w = self.win_ctrl.get_player_w_info()
        # 初始化黑棋的玩家信息
        if self.player_b == USER:
            self.label_4.setText("当前棋手：黑棋（账号用户）")
            self.label_6.setText(f"账号：  {self.act_b}")
            self.label_7.setText(f"用户名：{self.username_b}")
            self.label_9.setText(f"总场次：{self.AllPlays_b}")
            self.label_10.setText(f"胜场：  {self.WinPlays_b}")
        else:
            if self.player_b == VISTOR:
                self.label_4.setText("当前棋手：黑棋（游客）")
            elif self.player_b == AI_L1:
                self.label_4.setText("当前棋手：黑棋（一级AI）")
            elif self.player_b == AI_L2:
                self.label_4.setText("当前棋手：黑棋（二级AI）")
            self.label_6.setText(f"账号：  无")
            self.label_7.setText(f"用户名：无")
            self.label_9.setText(f"总场次：无")
            self.label_10.setText(f"胜场：  无")

        # 鼠标相关
        self.setCursor(Qt.PointingHandCursor)                   # 鼠标变成手指形状
        self.BlackPic = QPixmap('../designer/image/black.png')  # 黑棋图片
        self.WhitePic = QPixmap('../designer/image/white.png')  # 白棋图片
        self.mouse_point = LaBel(self)                          # 将鼠标图片改为棋子
        self.mouse_point.setScaledContents(True)                # 图片大小根据标签大小可变
        self.mouse_point.setGeometry(730, 380, 60, 60)  # 设置图片大小和坐标
        self.setMouseTracking(True)                             # 鼠标不按下时的移动也能捕捉到
        self.mouse_point.raise_()                               # 鼠标始终在最上层

        # 系统状态
        self.status = BLACK_PLAY                    # 棋局状态，黑棋先行
        self.mouse_point.setPixmap(self.BlackPic)   # 加载黑棋
        self.step = 0                               # 步数
        self.size = 8                               # 棋盘大小

        # 按钮类
        # 当有任意一个棋手是AI时，投降按钮改成AI行棋按钮
        if self.player_b == AI_L1 or self.player_b == AI_L2 or self.player_w == AI_L1 or self.player_w == AI_L2:
            self.yeildBtn.setText('AI行棋')
        self.yeildBtn.clicked.connect(self.yeild)           # 投降
        self.restartBtn.clicked.connect(self.restart)       # 重新开始
        self.recordBtn.clicked.connect(self.record)         # 录像

        # 计时器timer
        self.game_time = GameTime(self.label_3)
        self.game_time._signal.connect(self.set_time)
        self.game_time.set_status(1)
        self.game_time.start()

        # 棋盘：一行有self.size个chess，一共有self.size行
        self.chessboard = []
        self.chessLabels = []
        for row in range(self.size):    # 行循环
            chess_row = []              # 一行chess
            chessLabel_row = []         # 一行chess Label
            for col in range(self.size):  # 列循环
                # 每一个chess由{UI中的坐标}、{落子状态}和{一个LaBel对象}构成
                chess_temp = {'coord': {'x': 33+33+67*row, 'y': 27+34+66*col}, 'chess': IDLE}
                chess_row.append(chess_temp)
                chessLabel_temp = LaBel(self)
                chessLabel_temp.setVisible(True)  # 图片可视
                chessLabel_temp.setScaledContents(True)  # 图片大小根据标签大小可变
                chessLabel_row.append(chessLabel_temp)
            self.chessboard.append(chess_row)
            self.chessLabels.append(chessLabel_row)

        # 初始化中间的四个棋子
        ChessToAdd_list = []
        ChessToAdd_list.append((4, 3, BLACK))
        ChessToAdd_list.append((3, 4, BLACK))
        ChessToAdd_list.append((4, 4, WHITE))
        ChessToAdd_list.append((3, 3, WHITE))
        self.change_chessboard(ChessToAdd_list)




    # timer的槽函数：让label显示当前时间，实时更新
    def set_time(self,time):
        self.label_3.setText("时间：{}".format(time))



    # 鼠标移动event，移动鼠标时会触发
    def mouseMoveEvent(self, e):
        # 如果鼠标在棋盘范围内，则显示棋子图片
        if e.x() >= 0 and e.x() <= 600 and e.y() >= 0 and e.y() <= 600:
            self.mouse_point.move(e.x() - 30 , e.y() - 30)  # 棋子随鼠标移动
            self.mouse_point.show()
        # 否则隐藏棋子图片
        else:
            self.mouse_point.hide()



    # 鼠标点击event：玩家下棋。点击鼠标时会触发
    def mousePressEvent(self, e):
        # 若对局结束，则退出
        if self.status == END:
            return

        if self.check_IsAI():
            QMessageBox.information(self, "提示", "目前应当AI行棋！")
            return


        # 按下了左键
        if e.button() == Qt.LeftButton:
            # 检查落在位置是否在棋盘内，棋盘范围（40，40）~（960，960）
            if e.x() >= 40 and e.x() <= 600 and e.y() >= 40 and e.y() <= 600:
                # 获取鼠标点击位置所对应的chess在UI界面中的坐标，以及chessboard中的坐标
                chess_x, chess_y = self.get_coord(e.x(), e.y())
                # 如果未能确定棋子精确位置(x == -1)，或者该位置已有棋子(a!=0)，就不允许落子
                if chess_x == -1 or self.chessboard[chess_x][chess_y]['chess'] != IDLE:
                    QMessageBox.information(self, "提示", "当前位置已有落子！")
                    return
                # 每进行一次落子就获取当前可以被翻转棋子的列表
                turn_list = self.GetTrunList(chess_x, chess_y, self.status)
                # 空列表
                if turn_list == []:
                    QMessageBox.information(self, "提示", "当前位置不合法！")
                    return
                # 棋局更新
                self.update(turn_list)
                # 判断输赢（0：无人胜出， 1：黑棋手胜出， 2：白棋手胜出， 3：平局）
                self.judge()




    # 判断是否轮到AI。由AImove调用。
    def check_IsAI(self):
        # 轮到黑棋走了并且黑棋是AI
        if self.status == BLACK_PLAY and (self.player_b == AI_L1 or self.player_b == AI_L2):
            return True
        # 轮到白棋走了并且白棋是AI
        if self.status == WHITE_PLAY and (self.player_w == AI_L1 or self.player_w == AI_L2):
            return True

        return False



    # AI走一步。由yeild调用。
    def AImove(self):
        if self.status == END:
            return

        if self.check_IsAI() == False:
            QMessageBox.information(self, "提示", "当前未轮到AI落子！")
            return

        turn_list = []
        chess_x, chess_y = (0, 0)
        # 只要棋局没结束，当前的棋手一定有子可落
        if self.status == BLACK_PLAY:
            if self.player_b == AI_L1:      # 一级AI，随机选择合法的位置落子
                chess_x, chess_y = random.choice(self.get_valid_positions(BLACK))
            elif self.player_b == AI_L2:    # 二级AI，蒙特卡洛树搜索选择合法的位置落子
                chess_x, chess_y = random.choice(self.get_valid_positions(BLACK))
                # mcts = MCTS(self)
                # chess_x, chess_y = rvs.mctsNextPosition(self.chessboard)
            turn_list = self.GetTrunList(chess_x, chess_y, BLACK)
        elif self.status == WHITE_PLAY:
            if self.player_w == AI_L1:      # 一级AI，随机选择合法的位置落子
                chess_x, chess_y = random.choice(self.get_valid_positions(WHITE))
            elif self.player_w == AI_L2:    # 二级AI，蒙特卡洛树搜索选择合法的位置落子
                # chess_x, chess_y = random.choice(self.get_valid_positions(WHITE))
                # mcts = MCTS(self)
                chess_x, chess_y = rvs.mctsNextPosition(self.chessboard)
            turn_list = self.GetTrunList(chess_x, chess_y, WHITE)

        self.update(turn_list)
        # 判断输赢（0：无人胜出， 1：黑棋手胜出， 2：白棋手胜出， 3：平局）
        self.judge()


    # 获取鼠标点击位置所对应的chess在UI界面中的坐标，以及chessboard中的坐标。由mousePressEvent调用。
    def get_coord(self, m_x, m_y):
        # 遍历所有chess
        for row in range(self.size):
            for col in range(self.size):
                chess_temp = self.chessboard[row][col]
                dist = self.distance(m_x, m_y, chess_temp['coord']['x'], chess_temp['coord']['y'])

                # 与棋盘点的距离不超过32
                if dist <= 32:
                    return row, col

        return -1, -1  # 默认返回



    # 求两点距离。由get_coord调用。
    def distance(self, x1, y1, x2, y2):
        return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5



    # 修改棋盘状态。由init和update调用。
    def change_chessboard(self, ChessToChange_list):
        for (x, y, chess) in ChessToChange_list:
            pic = self.BlackPic  # 放置黑色棋子
            if chess == WHITE:
                pic = self.WhitePic  # 放置白色棋子
            # 放置棋子
            self.chessLabels[x][y].setPixmap(pic)
            # 设置位置，大小
            self.chessLabels[x][y].setGeometry(33 + 33 + 67 * x - 30, 27 + 34 + 66 * y - 30, 60,
                                               60)  # 减30是为了保证棋子处于棋盘格子中心位置
            # 显示
            self.chessLabels[x][y].show()
            self.chessboard[x][y]['chess'] = chess



    # 棋局更新。由mousePressEvent调用。
    def update(self, turn_list):
        self.step += 1
        self.label_2.setText("步数：{}".format(self.step))
        self.change_chessboard(turn_list)


    # 判断棋子是否在棋盘上。由GetTrunList调用。 
    def isOnBoard(self, x, y):
        return x >= 0 and x <= self.size-1 and y >= 0 and y <= self.size-1



    # 每进行一次落子就获取当前可以被翻转棋子的列表。由mousePressEvent和get_valid_positions调用
    def GetTrunList(self, chess_x, chess_y, chess):
        # 临时将chess放到指定的位置，方便判断哪些对手棋子可以被翻转
        self.chessboard[chess_x][chess_y]['chess'] = chess

        # 要被翻转的棋子列表
        turn_list = []

        # rival是chess的对手棋
        if chess == BLACK:
            rival = WHITE
        elif chess == WHITE:
            rival = BLACK
        else:
            return turn_list
        dir = [(-1,0),(1,0),(-1,1),(1,-1),(0,1),(0,-1),(1,1),(-1,-1)]    # 8个方向
        for x_dir, y_dir in dir:
            x, y = chess_x, chess_y
            x += x_dir
            y += y_dir
            if self.isOnBoard(x, y) and self.chessboard[x][y]['chess'] == rival:
                x += x_dir
                y += y_dir
                if not self.isOnBoard(x, y):
                    continue
                # 一直走到出界或不是对方棋子的位置
                while self.chessboard[x][y]['chess'] == rival:
                    x += x_dir
                    y += y_dir
                    if not self.isOnBoard(x, y):
                        break
                # 出界了，则没有棋子要翻转
                if not self.isOnBoard(x, y):
                    continue
                # 是自己的棋子，中间的所有棋子都要翻转
                if self.chessboard[x][y]['chess'] == chess:
                    while True:
                        x -= x_dir
                        y -= y_dir
                        # 回到了起点则结束
                        if x == chess_x and y == chess_y:
                            break
                        # 需要翻转的棋子
                        turn_list.append((x, y, chess))

        # 如果没有要被翻转的棋子，就前面临时放上的棋子去掉，即还原棋盘
        self.chessboard[chess_x][chess_y]['chess'] = IDLE
        if turn_list != []:
            turn_list.append((chess_x, chess_y, chess))

        return turn_list



    # 返回当前chess可以落子的所有位置。由judge和AImove调用
    def get_valid_positions(self, chess):
        positions = []
        # 遍历所有棋子，找出空棋子并判断
        for i in range(0, self.size):
            for j in range(0, self.size):
                if self.chessboard[i][j]['chess'] != IDLE:
                    continue
                if self.GetTrunList(i, j, chess):  # 不为空
                    positions.append((i, j))
        return positions



    # 返回当前chess在棋盘上的所有棋子数。由judge调用
    def count_chess_num(self, chess):
        chess_num = 0
        for i in range(0, self.size):
            for j in range(0, self.size):
                if self.chessboard[i][j]['chess'] == chess:
                    chess_num += 1

        return chess_num



    # 判断当前获胜的一方。由mousePressEvent调用
    def judge(self):
        black_pos_list = self.get_valid_positions(BLACK_PLAY)
        white_pos_list = self.get_valid_positions(WHITE_PLAY)
        # 双方均有子可走
        if black_pos_list != [] and white_pos_list != []:
            self.switch_status()    # 切换棋手
            return 0  # 无棋手胜出
        # 只有白方有子可走
        elif black_pos_list == [] and white_pos_list != []:
            self.status = BLACK_PLAY
            self.switch_status()    # 切换棋手
        # 只有黑方有子可走
        elif black_pos_list != [] and white_pos_list == []:
            self.status = WHITE_PLAY
            self.switch_status()  # 切换棋手
        # 双方均无子可走
        elif black_pos_list == [] and white_pos_list == []:
            black_chess_num = self.count_chess_num(BLACK_PLAY)
            white_chess_num = self.count_chess_num(WHITE_PLAY)
            if black_chess_num > white_chess_num:   # 黑棋手胜出
                self.end_game(BLACK_PLAY)
                return BLACK
            elif black_chess_num < white_chess_num: # 白棋手胜出
                self.end_game(WHITE_PLAY)
                return WHITE
            else:                                   # 平局
                return 3
        return 0    # 无棋手胜出



    # 切换棋手状态。由judge调用
    def switch_status(self):
        if self.status == BLACK_PLAY:
            self.mouse_point.setPixmap(self.WhitePic)  # 加载白棋
            self.ChessCan.setStyleSheet("background-image: url(:/bg/image/whites-removebg-preview.png);\n")
            self.status = WHITE_PLAY
            if self.player_w == USER:
                self.label_4.setText("当前棋手：白棋（账号）")
                self.label_6.setText(f"账号：  {self.act_w}")
                self.label_7.setText(f"用户名：{self.username_w}")
                self.label_9.setText(f"总场次：{self.AllPlays_w}")
                self.label_10.setText(f"胜场：  {self.WinPlays_w}")
            else:
                if self.player_w == VISTOR:
                    self.label_4.setText("当前棋手：白棋（游客）")
                elif self.player_w == AI_L1:
                    self.label_4.setText("当前棋手：白棋（一级AI）")
                elif self.player_w == AI_L2:
                    self.label_4.setText("当前棋手：白棋（二级AI）")
                self.label_6.setText(f"账号：  无")
                self.label_7.setText(f"用户名：无")
                self.label_9.setText(f"总场次：无")
                self.label_10.setText(f"胜场：  无")
        elif self.status == WHITE_PLAY:
            self.mouse_point.setPixmap(self.BlackPic)  # 加载黑棋
            self.ChessCan.setStyleSheet("background-image: url(:/bg/image/blacks-removebg-preview.png);\n")
            self.status = BLACK_PLAY
            if self.player_b == USER:
                self.label_4.setText("当前棋手：黑棋（账号）")
                self.label_6.setText(f"账号：  {self.act_b}")
                self.label_7.setText(f"用户名：{self.username_b}")
                self.label_9.setText(f"总场次：{self.AllPlays_b}")
                self.label_10.setText(f"胜场：  {self.WinPlays_b}")
            else:
                if self.player_b == VISTOR:
                    self.label_4.setText("当前棋手：黑棋（游客）")
                elif self.player_b == AI_L1:
                    self.label_4.setText("当前棋手：黑棋（一级AI）")
                elif self.player_b == AI_L2:
                    self.label_4.setText("当前棋手：黑棋（二级AI）")
                self.label_6.setText(f"账号：  无")
                self.label_7.setText(f"用户名：无")
                self.label_9.setText(f"总场次：无")
                self.label_10.setText(f"胜场：  无")



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
        self.result_label.setPixmap(pic)
        self.result_label.setGeometry(40, 80, 554, 174)




    # 认输。点击“投降”时调用
    def yeild(self):
        if self.player_b == AI_L1 or self.player_b == AI_L2 or self.player_w == AI_L1 or self.player_w == AI_L2:
            self.AImove()
        else:
            if self.status == END:
                QMessageBox.information(self, "提示", "棋局已结束，您无法认输！")
                return
            self.end_game(WHITE_PLAY if self.status == BLACK_PLAY else BLACK_PLAY)



    # 重新开始。点击“重新开始”时调用
    def restart(self):
        self.win_ctrl.switch_win(OTHELLO_2_START)



    # 保存录像。点击“保存录像”时调用
    def record(self):
        if self.step != 0:
            QMessageBox.information(self, "提示", "游戏已开始，无法录像！")
            return

        QMessageBox.information(self, "提示", "开始录像！")
        print("开始录像！")




    # 重写 closeEvent，当用户点击关闭按钮时自动返回开始录界面
    def closeEvent(self, event):
        self.win_ctrl.switch_win(OTHELLO_2_START)


    def keyPressEvent(self, event: QKeyEvent):
        # 检查是否按下空格键
        if event.key() == Qt.Key_Space:
            self.AImove()
