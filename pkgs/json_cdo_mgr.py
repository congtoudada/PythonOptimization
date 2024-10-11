# coding=utf-8
import random
import types
import sys
import os
import ujson

from copy import copy, deepcopy
from pkgs.cdo_mgr import CDOMgr


class UjsonCDOMgr(CDOMgr):

    def __init__(self):
        super(UjsonCDOMgr, self).__init__(suffix=".ujson")

    def _clone(self, cdo):
        """
        利用序列化替代深拷贝
        :param cdo:
        :return:
        """
        info_dict = cdo.__getstate__()
        # data = ujson.dumps(info_dict)
        # info_dict = ujson.loads(data)
        obj = copy(cdo)
        obj.__setstate__(info_dict)
        return obj


    def _save_cdo(self, cdo):
        """
        cdo序列化到本地
        :param cdo:
        :return:
        """
        if not hasattr(cdo, '__getstate__'):
            print("[ _save_cdo failed ] cdo is not serializable, please provide __getstate__")
            return False
        fullpath = os.path.join(self.cdo_folder, type(cdo).__name__ + self.cdo_suffix)
        info_dict = cdo.__getstate__()
        data = ujson.dumps(info_dict)
        with open(fullpath, 'w') as f:
            f.write(data)
        return True

    def _load_cdo(self, cls):
        """
        从本地反序列化为cdo
        :param cls:
        :return:
        """
        if not hasattr(cls, '__setstate__'):
            print("[ _load_cdo failed ] cdo is not deserializable, please provide __setstate__")
            return None
        fullpath = os.path.join(self.cdo_folder, cls.__name__ + self.cdo_suffix)
        if os.path.exists(fullpath):
            with open(fullpath, 'r') as f:
                data = f.read()  # 读取整个文件内容
                info_dict = ujson.loads(data)
                obj = cls()
                obj.__setstate__(info_dict)
                return obj
        else:
            print("[ _load_cdo failed ] Can't find cdo: " + fullpath)
            return None
