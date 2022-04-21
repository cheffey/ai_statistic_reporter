import decimal
from decimal import Decimal
from typing import Callable, TypeVar

from reporter.util.container import lst

Y = TypeVar('Y')


def rang(minIncluded: int, maxExcluded: int) -> lst[int]:
    return lst(range(minIncluded, maxExcluded))


def repeat(supplier: Callable[[], Y], times: int) -> lst[Y]:
    return rang(0, times).map(lambda x: supplier())


def todo(msg=''):
    raise Exception(f'TODO, Code NOT implement yet. {msg}')
