# coding=utf-8
from copy import copy, deepcopy

from test.player import Player
from utility.timer_kit import TimerKit

if __name__ == '__main__':
    versionNum = 2
    timerList = []
    playerList = []
    for i in range(versionNum):
        timerList.append(TimerKit(0))
        playerList.append(None)
    p = Player()
    for i in range(3):
        # 原始浅拷贝
        timerList[0].tic()
        playerList[0] = copy(p)
        timerList[0].toc()

        # 原始深拷贝
        timerList[1].tic()
        playerList[1] = deepcopy(p)
        timerList[1].toc()

    for i in range(versionNum):
        print("{0}: {1}".format(i, timerList[i].average_time))
        print(id(p.bestFriend) == id(playerList[i].bestFriend))
        print(id(p.data) == id(playerList[i].data))
        print(id(p.map) == id(playerList[i].map))
        print("*" * 50)



