# coding=utf-8
from obj.player import Player, compareResult
from pkgs.json_cdo_mgr import UJsonCDOMgr

p = Player("cong tou", level=3)  # 构造一个对象
p.init()  # 数据初始化（耗时操作）

ujsonMgr = UJsonCDOMgr.getinstance()  # 创建ujson cdo管理类
ujsonMgr.refresh_cdo(p, with_save=True)  # 刷新cdo及其缓存
ujsonMgr.warm_up()  # 预热cdo


p1 = ujsonMgr.create(Player)  # 通过cdoMgr生成一个对象
# 手动绑定共享部分
p1.bestFriend = p.bestFriend
p1.friends = p.friends

compareResult(p, p1)  # 比较二者差异
