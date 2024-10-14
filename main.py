# coding=utf-8
from obj.player import Player, compareResult
from pkgs.json_cdo_mgr import UJsonCDOMgr

# p = Player("cong tou", level=3)  # 构造一个对象
# p.init()  # 数据初始化（耗时操作）
#
# ujsonMgr = UJsonCDOMgr.getinstance()  # 创建ujson cdo管理类
# ujsonMgr.refresh_cdo(p, with_save=True)  # 刷新cdo及其缓存
# ujsonMgr.warm_up()  # 预热cdo
#
#
# p1 = ujsonMgr.create(Player)  # 通过cdoMgr生成一个对象
# # 手动绑定共享部分
# p1.bestFriend = p.bestFriend
# p1.friends = p.friends
#
# compareResult(p, p1)  # 比较二者差异

ujsonMgr = UJsonCDOMgr.getinstance()
ujsonMgr.warm_up()  # 预热cdo（在程序启动时调用一次即可，会对所有带@ex_warm_up的类进行预热）

# 自己构建一个类对象or获取已经缓存的cdo对象
# p = Player("cong tou", level=3)  # 构造一个对象
# p.init()  # 数据初始化（耗时操作）
player_cdo = ujsonMgr.get_cdo(Player)
# 做一些定制化操作
# ...

# 更新全局的CDO，如果想覆盖本地缓存，可以将with_save设为True
ujsonMgr.refresh_cdo(player_cdo, with_save=True)

# 正常构建对象，就是修改后CDO的版本
p1 = ujsonMgr.create(Player)

# 删除全局的CDO，如果也想删除本地缓存，可以将with_file设为True
ujsonMgr.release_cdo(Player, with_file=True)
