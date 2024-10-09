# coding=utf-8
# V1: 只测试到ujson序列化
# 1.导包
import random
import pickle
import types

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
n = 1000  # 数据规模
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
        self.bestFriend = Friend(10)
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

serialize_dict = {}


def my_serialize(obj):
    t = type(obj)
    t_str = str(t)
    if serialize_dict.__contains__(t_str):
        return serialize_dict[t_str](obj)
    else:
        print('serialize_dict不存在该类型的序列化方法: ' + t_str)
        return None


def _friend_serialize(obj):
    state = {}
    state.update(obj.__dict__)
    return state


def _player_serialize(obj):
    state = {}
    # 属于浅拷贝
    state.update(obj.__dict__)
    # ujson容错能力较差，序列化时如果遇到函数会报错
    for k, v in state.items():
        if isinstance(v, types.FunctionType):
            state[k] = None
    # 复杂类型需要自己序列化
    state['bestFriend'] = my_serialize(obj.bestFriend)
    state['friends'] = []
    for i in range(len(obj.friends)):
        state['friends'].append(my_serialize(obj.friends[i]))
    return state


serialize_dict[str(Player)] = _player_serialize
serialize_dict[str(Friend)] = _friend_serialize

deserialize_dict = {}


def my_deserialize(target_type, dict_info):
    if not isinstance(target_type, str):
        target_type = str(target_type)
    if deserialize_dict.__contains__(target_type):
        return deserialize_dict[target_type](dict_info)
    else:
        print('deserialize_dict不存在该类型的反序列化方法: ' + target_type)
        return None


def _friend_deserialize(info_dict):
    friend = Friend(0)
    friend.__dict__.update(info_dict)
    return friend


def _player_deserialize(info_dict):
    # 如果对象构建本身比较耗时，可以通过缓存一个全局对象，接着使用copy拷贝一份，再手动反序列化需要的地方
    player = Player()
    # player.__dict__.update(info_dict)  # 这样会丢失函数信息
    for k, v in info_dict.items():
        if v is not None:
            player.__dict__[k] = v
    player.bestFriend = my_deserialize(Friend, info_dict['bestFriend'])
    player.friends = []
    for i in range(len(info_dict['friends'])):
        player.friends.append(my_deserialize(Friend, info_dict['friends'][0]))
    player.dataMap = {}
    for k, v in info_dict['dataMap'].items():
        player.dataMap[int(k)] = v
    return player


deserialize_dict[str(Player)] = _player_deserialize
deserialize_dict[str(Friend)] = _friend_deserialize

serialize_str = json.dumps(p, default=my_serialize)  # 对象序列化为字符串
# print(serialize_p)
info_dict = json.loads(serialize_str)  # 字符串反序列化为字典
# 注意：dataMap的key是字符串
# print(info_dict)
# url: https://blog.csdn.net/loethen/article/details/138501948
# f = _friend_deserialize(info_dict['bestFriend'])
p5 = my_deserialize(Player, info_dict)  # 字典反序列化为对象
print(p5.play)
compareResult(p, p5)

serialize_dict = my_serialize(p)  # 对象序列化为字典
serialize_str2 = ujson.dumps(serialize_dict)  # 字典序列化为字符串
info_dict2 = ujson.loads(serialize_str2)  # 反序列化为字典
p6 = my_deserialize(Player, info_dict2)
compareResult(p, p6)
