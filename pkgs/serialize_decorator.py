# coding=utf-8
"""
--------------------------- 复合类型序列化函数 ---------------------------
"""
import types
from copy import copy

_complex_serialize_dispatcher = {}
_none_serialize_set = {types.FunctionType}


def _serialize_list(_l):
    if not isinstance(_l, list):
        print('_serialize_list failed! param is not list!')
        return _l
    if len(_l) == 0:
        return _l
    _l = copy(_l)
    # 处理复合类型
    if _complex_serialize_dispatcher.__contains__(type(_l[0])):
        for i in range(len(_l)):
            _l[i] = _complex_serialize_dispatcher[type(_l[i])](_l[i])
    # 处理自定义类型
    elif hasattr(_l[0], '__getstate__'):
        for i in range(len(_l)):
            _l[i] = _l[i].__getstate__()
    return _l


_complex_serialize_dispatcher[list] = _serialize_list


def _serialize_dict(_d):
    if not isinstance(_d, dict):
        print('_serialize_dict failed! param is not dict!')
        return _d
    if len(_d) == 0:
        return _d
    _d = copy(_d)
    # 这里为了简化，只考虑value的序列化
    for k, v in _d.items():
        # 处理复合类型
        if _complex_serialize_dispatcher.__contains__(type(v)):
            _d[k] = _complex_serialize_dispatcher[type(v)](v)
        # 处理自定义类型
        elif hasattr(v, '__getstate__'):
            _d[k] = v.__getstate__()
        else:
            break
    return _d


_complex_serialize_dispatcher[dict] = _serialize_dict


def _serialize_set(_s):
    if not isinstance(_s, set):
        print('_serialize_set failed! param is not set!')
        return _s
    if len(_s) == 0:
        return list(_s)
    _l = list(_s)
    _s = _serialize_list(_l)
    return _s


_complex_serialize_dispatcher[set] = _serialize_set


def ex_serialize(cls):
    def __getstate__(self):
        d = {}
        for slot in cls.__slots__:
            o = getattr(self, slot)
            if o is None:
                continue
            if _none_serialize_set.__contains__(type(o)):
                continue
            # 复合类型
            if _complex_serialize_dispatcher.__contains__(type(o)):
                d[slot] = _complex_serialize_dispatcher[type(o)](o)
            # 自定义类型
            elif hasattr(o, '__getstate__'):
                d[slot] = o.__getstate__()
            # 其他类型
            else:
                d[slot] = o
        return d

    cls.__getstate__ = __getstate__
    return cls
