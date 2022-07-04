import logging
from functools import reduce
from typing import Iterable, TypeVar, Callable, overload, Mapping, List, Tuple, Dict

X = TypeVar('X')
Y = TypeVar('Y')
Z = TypeVar('Z')


class lst(List[X]):
    def __init__(self, data: Iterable[X] = None):
        if data is None:
            data = []
        if not isinstance(data, Iterable):
            data = [data]
        super().__init__(data)

    def append(self, ele: X) -> 'lst[X]':
        super().append(ele)
        return self

    def insert(self, idx, ele: X) -> 'lst[X]':
        super().insert(idx, ele)
        return self

    def map(self, func: Callable[[X], Y]) -> 'lst[Y]':
        return lst[Y](map(func, self))

    def to_dic(self, func: Callable[[X], Tuple[Y, Z]]) -> 'dic[Y,Z]':
        return dic(map(func, self))

    def sorted(self, **kwargs) -> 'lst[X]':
        return lst[X](sorted(self, **kwargs))

    def reverse(self) -> 'lst[X]':
        super().reverse()
        return self

    def foreach(self, func) -> None:
        for ele in self:
            func(ele)

    def filter(self, func) -> 'lst[X]':
        return lst[X](filter(func, self))

    def count(self, func) -> int:
        return len(lst(filter(func, self)))

    def reduce(self, func: Callable[[X, X], Y], default) -> Y:
        if len(self) == 0:
            return default
        return reduce(func, self)

    def flat_map(self, spliter: Callable[[X], Iterable[Y]]) -> 'lst[Y]':
        result = []
        for ele in self:
            result.extend(spliter(ele))
        return lst(result)

    def join_to_string(self, seperator='') -> str:
        return self.reduce(lambda x, y: f'{x}{seperator}{y}', '')

    @overload
    def __getitem__(self, i) -> X:
        ...

    @overload
    def __getitem__(self, s: slice) -> 'lst[X]':
        ...

    def __getitem__(self, input):
        if isinstance(input, slice):
            return lst(super().__getitem__(input))
        else:
            value = super().__getitem__(input)
            return value

    def __add__(self, other: 'lst[Y]') -> 'lst[X|Y]':
        return lst(super().__add__(other))

    def __sub__(self, other):
        res = lst(self)
        for ele in other:
            if ele in res:
                res.remove(ele)
            else:
                logging.error(f"ele: {ele} in lst: {other} is NOT in lst: {self} when subtract")
        return res

    def first(self, rule=lambda x: True) -> X:
        for ele in self:
            if rule(ele):
                return ele
        return None

    def last(self) -> X:
        if len(self) == 0:
            return None
        return self[len(self) - 1]

    def min(self, comparator=lambda x: x, default=None) -> X:
        return min(self, key=comparator, default=default)

    def max(self, comparator=lambda x: x, default=None) -> X:
        return max(self, key=comparator, default=default)

    def any(self, rule) -> bool:
        for ele in self:
            if rule(ele):
                return True
        return False

    @classmethod
    def of(cls, *args):
        return lst(args)

    def map_to_dic(self, k_func, v_func) -> 'dic[object,object]':
        rtn = dic()
        for ele in self:
            key = k_func(ele)
            value = v_func(ele)
            rtn[key] = value
        return rtn

    def group_by(self, func, sort=False) -> 'dic[object,lst[X]]':
        rtn = dic()
        for ele in self:
            key = func(ele)
            group = rtn.get_or_insert(key, lst())
            group.append(ele)
        if sort:
            group = rtn.pairs().sorted(key=lambda x: x[0])
            rtn = dic(group)
        return rtn

    def split(self, func1, func2) -> Tuple['lst', 'lst']:
        rtn1, rtn2 = lst(), lst()
        for ele in self:
            value1 = func1(ele)
            value2 = func2(ele)
            rtn1.append(value1)
            rtn2.append(value2)
        return rtn1, rtn2

    def without_duplicate(self) -> 'lst[X]':
        rtn = lst()
        for ele in self:
            if ele not in rtn:
                rtn.append(ele)
        return rtn

    def get(self, index: int, default=None):
        if len(self) > index:
            return self[index]
        return default


K = TypeVar('K')
V = TypeVar('V')
W = TypeVar('W')


class dic(Dict[K, V]):
    @staticmethod
    def zip(keys, values):
        return dic(zip(keys, values))

    @property
    def __dict__(self):
        return self

    def pairs(self) -> lst[Tuple[K, V]]:
        return self.keys().map(lambda x: (x, self[x]))

    def __getattribute__(self, item):
        try:
            return super().__getattribute__(item)
        except AttributeError as e:
            if item in self:
                return self[item]
            raise e

    def __setattr__(self, key, value):
        self[key] = value

    def values(self) -> lst[V]:
        return lst(super().values())

    def keys(self) -> lst[K]:
        return lst(super().keys())

    # this function has serious performance defect
    def filter(self, func: Callable[[K, V], object]) -> 'dic[K,V]':
        result = dic()
        for key in self.keys():
            value = self[key]
            if func(key, value):
                result[key] = value
        return result

    def map_lst(self, value_call: Callable[[K, V], W]) -> 'lst[W]':
        result = lst()
        for key in self.keys():
            value = self[key]
            new_value = value_call(key, value)
            result.append(new_value)
        return result

    def map_dic(self, value_call: Callable[[K, V], W]) -> 'dic[K,W]':
        result = dic()
        for key in self.keys():
            value = self[key]
            new_value = value_call(key, value)
            result[key] = new_value
        return result

    def sorted(self, key: Callable[[K, V], object], reverse: bool = False) -> 'dic[K,V]':
        pairs_sorted = self.pairs().sorted(key=lambda x: key(x[0], x[1]), reverse=reverse)
        return dic(pairs_sorted)

    def get_or_insert(self, k: K, else_v: V) -> V:
        if k in self:
            return self[k]
        else:
            self[k] = else_v
            return else_v


def _wrap(value):
    if isinstance(value, Mapping):
        return dic(value)
    if isinstance(value, str):
        return value
    if isinstance(value, Iterable):
        return lst(value)
    return value


if __name__ == '__main__':
    to_dic = lst(['a', 'b', 'C', 'D']).to_dic(lambda x: (x, x + 'x'))
    print(to_dic)
    print(to_dic.a)
    attr = getattr(to_dic, 'item')

# print(to_dic.a)
