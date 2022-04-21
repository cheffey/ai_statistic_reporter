from typing import Union

from reporter.model.percentage import Percentage
from reporter.util.container import dic


def _html_color(text, color="red"):
    return f'<font color="{color}">{text}</font>'


colors = 'green', 'orange', 'red'
DARK_PURPLE = '#C71585'

_DEFAULT_color = 'black'


class ColorStrategy:
    def __init__(self, **kwargs):
        self.limit_color = dic.zip(kwargs.values(), kwargs.keys())
        self.limits = self.limit_color.keys().sorted(reverse=True)
        assert len(kwargs) == len(self.limit_color), f'duplicated color bound value: {kwargs}'

    def color_of(self, num: Union[int, float]):
        for limit in self.limits:
            if num >= limit:
                color_name = self.limit_color[limit]
                try:
                    return eval(color_name)
                except NameError:
                    return color_name
        return _DEFAULT_color

    def html_color(self, num: Union[int, float], string: str = None):
        if string is None:
            string = num
        color = self.color_of(num)
        return _html_color(string, color)

    def perc_color(self, per: Percentage):
        return self.html_color(per.value, per.value_str)


DEFAULT_PERCENTAGE_COLOR_STRATEGY = ColorStrategy(blue=0.99, green=0.95, orange=0.9, red=0.0, DARK_PURPLE=-1)
DEFAULT_DATA_SIZE_COLOR_STRATEGY = ColorStrategy(blue=200, green=100, red=0)
NO_COLOR_STRATEGY = ColorStrategy()

if __name__ == '__main__':
    a = ColorStrategy(blue=0.95, green=0.95, orange=0.9, red=0.0, DARK_PURPLE=-1)
    print()
