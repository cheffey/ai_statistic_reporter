import sys
from typing import Union

from reporter.model.abs.cmp import Comparable


class Percentage(Comparable):
    def __init__(self, a: Union[int, float], b: Union[int, float] = 1):
        self.a = a
        self.b = b

    def __compare_by__(self):
        return self.value

    def desc_value(self):
        return self.desc, self.value

    @property
    def value(self):
        if self.b == 0:
            if self.a > 0:
                return sys.maxsize
            else:
                return -1
        return self.a / self.b

    @property
    def desc(self) -> str:
        return f'{self.a}/{self.b}'

    @property
    def value_str(self):
        if self.value == sys.maxsize:
            return '∞'
        elif self.value == -1:
            return 'N/A'
        else:
            return f'{round(self.value * 100, 2)}%'

    def __str__(self) -> str:
        return f'{self.value_str}({self.a}/{self.b})'

    def is_division_by_zero(self):
        return self.b == 0
