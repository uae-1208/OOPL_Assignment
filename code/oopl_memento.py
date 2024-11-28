# 备忘录类，用于存储状态
class Memento:
    def __init__(self, dic_state):
        # 私有属性保存状态，用一个字典囊括：1.棋盘状态 2.步数step 3.当前棋手 4.上一步落子的坐标
        self._state = dic_state

    def get_state(self):
        return self._state


# 原发器类，表示需要保存状态的对象：棋局状态
class GameState:
    def __init__(self):
        self._state = {}    # 空字典

    # 返回系统状态
    def get_sys_state(self):
        return self._state

    # 保存当前状态为备忘录
    def save(self):
        return Memento(self._state)

    # 从备忘录恢复状态
    def restore(self, memento):
        self._state = memento.get_state()


# 管理者类，负责管理备忘录
class Caretaker:
    def __init__(self):
        self._history = []  # 备忘录历史

    # 保留记录
    def save(self, memento):
        self._history.append(memento)

    # 读取记录
    def undo(self):
        if not self._history:
            return None
        return self._history.pop()

