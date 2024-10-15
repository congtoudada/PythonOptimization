# coding=utf-8
import types, weakref
from copy import copy, deepcopy

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
        else:  # 遇到未见类
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
        else:  # 遇到未见类
            ret[key] = deepcopy(value)
    return ret


_my_deepcopy_dispatcher[dict] = _copy_dict


def quick_deepcopy(obj):
    """
    快速深拷贝，对于复合类型自己操作深拷贝能使得速度更快
    :param obj:
    :return:
    """
    cp = _my_deepcopy_dispatcher.get(type(obj))
    if cp is None:
        return deepcopy(obj)
    else:
        return cp(obj)
