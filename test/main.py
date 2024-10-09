# coding=utf-8
# 1.导包
import random
import pickle
import ujson
import json

from copy import copy, deepcopy

# 2.定义测试对象
class Friend(object):
    def __init__(self, fid):
        self.owner = None  # 用于构建环形依赖
        self.fid = fid
        self.love = random.randint(1, 100)

# # 构造函数内生成数据
# n = 500  # 数据规模
# class Player(object):
#     def __init__(self):
#         self.name = "cong tou"
#         self.hp = 101.5
#         self.lv = 1
#         self.data = [random.randint(10000, 1000000) for _ in range(n)]
#         self.dataMap = {}
#         self.skills = [{"1001": "普通攻击"}, {"1002": "战技"}, {"1003": "大招"}]
#         self.bag = {"10001": 10, "10002": 0, "10003": 100}
#         self.bestFriend = Friend(0)
#         self.friends = [Friend(random.randint(10000, 1000000)) for _ in range(n)]
#         self.play = playFunc
#         # self.brother = None  # 用于构建自依赖
#         for i in range(n):
#             self.dataMap[i] = [random.randint(10, 100) for _ in range(random.randint(1, 100))]

#     def __str__(self):
#         return "Player name: {0}, hp: {1}".format(str(self.name), str(self.hp))

# 预先生成数据
n = 100  # 数据规模
data = [random.randint(10000, 1000000) for _ in range(n)]
dataMap = {}
friends = [Friend(random.randint(10000, 1000000)) for _ in range(n)]
for i in range(n):
    dataMap[i] = [random.randint(10, 100) for _ in range(random.randint(1, 100))]


def playFunc():
    print("Playing")


class Player(object):
    def __init__(self):
        self.name = "cong tou"
        self.hp = 101.5
        self.lv = 1
        self.data = data
        self.dataMap = dataMap
        self.skills = [1001, 1002, 1003]
        self.bag = {"10001": 10, "10002": 0, "10003": 100}
        self.bestFriend = Friend(0)
        self.friends = friends
        self.play = playFunc
        # self.brother = None  # 用于构建自依赖

    def __str__(self):
        return "Player name: {0}, hp: {1}".format(str(self.name), str(self.hp))


# 打印函数
def compareResult(p1, p2):
    print('地址比较: ')
    print("bestFriend: " + str(id(p1.bestFriend) == id(p2.bestFriend)))  # 共享(True)
    print("friends[0]: " + str(id(p1.friends[0]) == id(p2.friends[0])))  # 共享(True)
    print("playFunc: " + str(id(p1.play) == id(p2.play)))  # 共享(True)
    print("friends: " + str(id(p1.friends) == id(p2.friends)))  # 拷贝(False)
    print("data: " + str(id(p1.data) == id(p2.data)))  # 拷贝(False)
    print("dataMap: " + str(id(p1.dataMap) == id(p2.dataMap)))  # 拷贝(False)
    print("hp: " + str(id(p1.hp) == id(p2.hp)))  # 拷贝(False)
    print("*" * 50)
    print('数值比较: ')
    print('friends[0]: ' + str(p1.friends[0].love == p2.friends[0].love))
    print('data[0]: ' + str(p1.data[0] == p2.data[0]))
    print('dataMap[0]: ' + str(p1.dataMap[0] == p2.dataMap[0]))
    print('skills[0]: ' + str(p1.skills[0] == p2.skills[0]))


# 3.构建测试对象，开始测试
p = Player()

# 浅拷贝
print('------------ 浅拷贝 ------------')
p1 = copy(p)
compareResult(p, p1)

# 深拷贝
print('------------ 深拷贝 ------------')
p2 = deepcopy(p)
compareResult(p, p2)

# pickle序列化（很慢，比深拷贝还慢）
# print('------------ pickle序列化 ------------')
# s_data = pickle.dumps(p)
# p3 = pickle.loads(s_data)

# compareResult(p, p3)
# print(p.hp)
# print(p3.hp)

# 自定义深拷贝
print('------------ 自定义深拷贝 ------------')
import types, weakref
_my_deepcopy_dispatcher = {}

def _copy_immutable(x):
    """
    1.对于常见基础类型，直接返回（参考copy源码）
    """
    return x
for t in (type(None), int, long, float, bool, str, tuple,
          frozenset, type, xrange, types.ClassType,
          types.BuiltinFunctionType, type(Ellipsis),
          types.FunctionType, weakref.ref):
    _my_deepcopy_dispatcher[t] = _copy_immutable
for name in ("ComplexType", "UnicodeType", "CodeType"):
    t = getattr(types, name, None)
    if t is not None:
        _my_deepcopy_dispatcher[t] = _copy_immutable

def _copy_list(_l):
    """
    2.对于数组类型：拷贝新数组，逐一深拷贝
    """
    ret = copy(_l)
    for idx, item in enumerate(ret):
        cp = _my_deepcopy_dispatcher.get(type(item))
        if cp is not None:
            ret[idx] = cp(item)
        else:  # 遇到未见类：可选择深拷贝，也可以选择跳过
            ret[idx] = deepcopy(item)
    return ret
_my_deepcopy_dispatcher[list] = _copy_list

def _copy_dict(d):
    """
    3.对于字典类型：拷贝新字典，逐一深拷贝
    """
    ret = copy(d)
    for key, value in ret.items():
        cp = _my_deepcopy_dispatcher.get(type(value))
        if cp is not None:
            ret[key] = cp(value)
        else:  # 遇到未见类：可选择深拷贝，也可以选择跳过
            ret[key] = deepcopy(value)
    return ret
_my_deepcopy_dispatcher[dict] = _copy_dict

def my_deepcopy(obj):
    cp = _my_deepcopy_dispatcher.get(type(obj))
    if cp is None:
        return deepcopy(obj)
    else:
        return cp(obj)


class Friend(object):
    def __init__(self, fid):
        self.owner = None  # 用于构建环形依赖
        self.fid = fid
        self.love = random.randint(1, 100)

    def __deepcopy__(self, memo):
        ret = copy(self)
        ret.love = my_deepcopy(self.love)
        return ret


class Player(object):
    def __init__(self):
        self.name = "cong tou"
        self.hp = 101.5
        self.lv = 1
        self.data = data
        self.dataMap = dataMap
        self.skills = [1001, 1002, 1003]
        self.bag = {"10001": 10, "10002": 0, "10003": 100}
        self.bestFriend = Friend(0)
        self.friends = friends
        self.play = playFunc
        # self.brother = None  # 用于构建自依赖

    def __deepcopy__(self, memo):
        # 手动拷贝每个属性应该最快，但是太繁琐，没有实际意义
        # 当前做法是:
        #   - 1.先执行一次浅拷贝构造对象
        #   - 2.利用自定义快速拷贝函数来替代深拷贝（直到遇见未见类再使用deepcopy或跳过）
        ret = copy(self)  # 执行一次浅拷贝，把基础类型拷贝了
        ret.data = my_deepcopy(self.data)
        ret.dataMap = my_deepcopy(self.dataMap)
        ret.skills = my_deepcopy(self.skills)
        ret.bag = my_deepcopy(self.bag)
        ret.bestFriend = my_deepcopy(self.bestFriend)
        ret.friends = my_deepcopy(self.friends)
        return ret

    def __str__(self):
        return "Player name: {0}, hp: {1}".format(str(self.name), str(self.hp))


p = Player()

p4 = my_deepcopy(p)  # 内部会调用deepcopy(p)
compareResult(p, p4)
