_dispatcher = {}


def _copy_list(_l):
    ret = _l.copy()
    for idx, item in enumerate(ret):
        cp = _dispatcher.get(type(item))
        if cp is not None:
            ret[idx] = cp(item)
    return ret


_dispatcher[list] = _copy_list


def _copy_dict(d):
    ret = d.copy()
    for key, value in ret.items():
        cp = _dispatcher.get(type(value))
        if cp is not None:
            ret[key] = cp(value)

    return ret


_dispatcher[dict] = _copy_dict


def deepcopy_v1(obj):
    cp = _dispatcher.get(type(obj))
    if cp is None:
        return obj
    else:
        return cp(obj)
