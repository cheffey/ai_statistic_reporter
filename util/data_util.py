from types import SimpleNamespace
from typing import Iterable, TypeVar

from reporter.util.container import dic, lst

T = TypeVar('T')


# fake clone to dic
def clone(clonee: T) -> dic:
    return _clone(clonee)


def _clone(clonee):
    if isinstance(clonee, dict):
        rtn = dic()
        for k in clonee:
            v = clonee[k]
            rtn[k] = _clone(v)
        return rtn
    if isinstance(clonee, str):
        return clonee
    if isinstance(clonee, Iterable):
        rtn = lst()
        for ele in clonee:
            rtn.append(_clone(ele))
        return rtn
    if hasattr(clonee, '__dict__'):
        rtn = dic()
        d = clonee.__dict__
        for key in d.keys():
            rtn[key] = _clone(d[key])
        return rtn
    return clonee
