# coding=utf-8
import random

class Friend(object):
    def __init__(self, id):
        self.id = id
        self.love = random.randint(1, 100)

n = 500
data = [random.randint(10000, 1000000) for _ in range(n)]
map = {}
friends = [Friend(random.randint(10000, 1000000)) for _ in range(n)]
for i in range(n):
    map[i] = [random.randint(10, 100) for _ in range(random.randint(1, 100))]


class Player(object):
    def __init__(self):
        self.hp = 12345.0
        self.lv = 60
        self.skills = [1001, 1002, 1003]
        self.bag = {"10001": 10, "10002": 0, "10003": 100}
        self.data = data
        self.map = map
        self.bestFriend = Friend(0)
        self.friends = friends


    def __str__(self):
        return "Player hp: {0}, lv: {1}".format(str(self.hp), str(self.lv))
