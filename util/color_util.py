import dataclasses
import random
from enum import Enum


class ColorTendency(Enum):
    REDISH = lambda r, g, b: r > g + 10 and r > b + 10
    GREENISH = lambda r, g, b: g > r + 10 and g > b + 10
    BLUEISH = lambda r, g, b: b > r + 10 and b > g + 10
    LIGHT = lambda r, g, b: r > 230 and b > 230 and g > 230


def has_close_color_in(color, skip_colors):
    red0, green0, blue0 = color
    for red, green, blue in skip_colors:
        if abs(red0 - red) < 50 and abs(green0 - green) < 50 and abs(blue0 - blue) < 50:
            return True
    return False


def bld_color(seed, color_tendency: ColorTendency) -> 'Color':
    try:
        random.seed(seed)
        while True:
            skip_colors = [(0, 0, 0)]
            red = random.randint(0, 255)
            green = random.randint(0, 255)
            blue = random.randint(0, 255)
            if not has_close_color_in((red, green, blue), skip_colors) \
                    and color_tendency(red, green, blue):
                return Color(red, green, blue)
    finally:
        random.seed()


@dataclasses.dataclass
class Color:
    red: int
    green: int
    blue: int

    def hex_form(self):
        return f"#{_as_hex(self.red)}{_as_hex(self.green)}{_as_hex(self.blue)}"

    def rgb_form(self):
        return f"rgb({self.red}, {self.green}, {self.blue})"


def _as_hex(oct):
    hex_str = hex(oct)[2:4]
    if len(hex_str) == 1:
        hex_str = '0' + hex_str
    return hex_str


if __name__ == '__main__':
    color2 = bld_color(1, ColorTendency.REDISH)
    print(color2)
