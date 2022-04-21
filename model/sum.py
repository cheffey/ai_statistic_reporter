from reporter.model.abs.cmp import Comparable


class Sum(Comparable):

    def __init__(self, a, b):
        self.a = a
        self.b = b

    def desc_value(self):
        return self.desc, self.value

    @property
    def value(self):
        return self.a + self.b

    @property
    def desc(self) -> str:
        return f'({self.a}+{self.b})'

    def __str__(self) -> str:
        return f'{self.value}{self.desc}'

    def __compare_by__(self):
        return self.value

    def __add__(self, other: 'Sum') -> 'Sum':
        return Sum(self.a + other.a, self.b + other.b)
