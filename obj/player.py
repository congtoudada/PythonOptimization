# coding=utf-8
import random
import time

from obj.friend import Friend
from pkgs.serialize_decorator import ex_serialize

n = 3


def playFunc():
    print("Playing")


@ex_serialize
class Player(object):
    __slots__ = ('name', 'version', 'is_active', 'level', 'health', 'position', 'callback', 'data', 'equipment', 'bag',
                 'skills', 'dataMap', 'bestFriend', 'friends', 'bro')

    def __init__(self, name="cong tou", level=1):
        # -------------------------- python内置类型 --------------------------
        self.name = name  # str
        self.version = "v0.1"  # str
        self.is_active = True  # bool
        self.level = level  # int
        self.health = 13.14  # float
        self.position = (0, 0, 0)  # tuple
        self.callback = playFunc  # Function类型
        self.data = []  # list[int]
        self.equipment = set()  # set[int]
        self.bag = {"10001": 10, "10002": 0, "10003": 100}  # dict[str]=int
        self.skills = [{"1001": "普通攻击".decode('utf-8')},
                       {"1002": "战技".decode('utf-8')},
                       {"1003": "大招".decode('utf-8')}]  # list[dict[str]=str]
        self.dataMap = {}  # dict[int] = list[int]
        # -------------------------- python自定义1类型 --------------------------
        self.bestFriend = None  # 自定义类型
        self.friends = []  # list[自定义类型]
        self.bro = None  # 用于构建自依赖
        self.init()

    def init(self):
        self.data = [random.randint(10000, 1000000) for _ in range(n)]
        self.equipment = set(self.data)
        for i in range(n):
            self.dataMap[i] = [random.randint(10, 100) for _ in range(random.randint(1, 100))]
        self.bestFriend = Friend()
        self.friends = [Friend() for _ in range(n)]
        time.sleep(1)  # 模拟耗时计算

    def __setstate__(self, state):
        # -------------------------- python内置类型 --------------------------
        self.name = state['name']
        self.version = state['version']
        self.is_active = bool(state['is_active'])
        self.level = int(state['level'])
        self.health = float(state['health'])
        self.position = tuple(state['position'])
        self.callback = playFunc  # Function类型
        self.data = state['data']
        self.equipment = set(state["equipment"])
        self.bag = state['bag']
        self.skills = self.skills = [{key: value} for item in state['skills'] for key, value in item.items()]
        self.dataMap = {}
        for k, v in state['dataMap'].items():
            self.dataMap[int(k)] = v
        # -------------------------- python自定义类型 --------------------------
        fri = Friend()
        fri.__setstate__(state["bestFriend"])
        self.bestFriend = fri
        # 我希望friends能共享，不反序列化
        # self.friends = []
        # for i in range(len(state["friends"])):
        #     fri = Friend()
        #     fri.__setstate__(state["friends"][i])
        #     self.friends.append(fri)


def compareResult(p1, p2):
    print('地址比较: ')
    print("bestFriend: " + str(id(p1.bestFriend) == id(p2.bestFriend)))
    print("friends[0]: " + str(id(p1.friends[0]) == id(p2.friends[0])))
    print("playFunc: " + str(id(p1.callback) == id(p2.callback)))
    print("friends: " + str(id(p1.friends) == id(p2.friends)))
    print("data: " + str(id(p1.data) == id(p2.data)))
    print("dataMap: " + str(id(p1.dataMap) == id(p2.dataMap)))
    print("health: " + str(id(p1.health) == id(p2.health)))
    print("*" * 50)
    print('数值比较: ')
    print('friends[0].fid: ' + str(p1.friends[0].fid == p2.friends[0].fid))
    print('friends[0].show[0]: ' + str(p1.friends[0].show[0] == p2.friends[0].show[0]))
    print('data[0]: ' + str(p1.data[0] == p2.data[0]))
    print('dataMap[0]: ' + str(p1.dataMap[0] == p2.dataMap[0]))
    print('skills[0]: ' + str(p1.skills[0] == p2.skills[0]))
    print('name: ' + str(p1.name == p2.name))
    print("-" * 50)
