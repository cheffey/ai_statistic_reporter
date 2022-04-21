import abc


def _value_of(comparable):
    if isinstance(comparable, int):
        return comparable
    elif isinstance(comparable, float):
        return comparable
    elif isinstance(comparable, Comparable):
        return _value_of(comparable.__compare_by__())
    else:
        raise Exception(f'Unsupported type: {type(comparable)}')


class Comparable(abc.ABC):
    @abc.abstractmethod
    def __compare_by__(self):
        pass

    def __gt__(self, other):
        return _value_of(self) - _value_of(other) > 0

    def __ge__(self, other):
        return _value_of(self) - _value_of(other) >= 0

    def __le__(self, other):
        return _value_of(self) - _value_of(other) <= 0

    def __lt__(self, other):
        return _value_of(self) - _value_of(other) < 0

    def __eq__(self, other):
        return _value_of(self) - _value_of(other) == 0
