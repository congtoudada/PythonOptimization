# coding=utf-8
from obj.player import Player, compareResult
from pkgs.json_cdo_mgr import UjsonCDOMgr

ujsonMgr = UjsonCDOMgr()  # 创建ujson cdo管理类
ujsonMgr.release_cdo(Player, with_file=True)  # 删除cdo，同时删除本地缓存
p = Player("cong tou", level=3)  # 构造一个对象
ujsonMgr.set_cdo(p, with_save=True)  # 设置cdo，同时缓存
p1 = ujsonMgr.create(Player)  # 通过cdoMgr生成一个对象
compareResult(p, p1)  # 比较二者差异
