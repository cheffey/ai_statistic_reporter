class Box:
    def __init__(self, x, y, w, h, clazz):
        self.clazz = clazz
        self.x = x
        self.y = y
        assert w >= 0
        assert h >= 0
        self.w = w
        self.h = h


class ResBox(Box):
    def __init__(self, x, y, w, h, clazz, score=None):
        super().__init__(x, y, w, h, clazz)
        self.score = score

    def __str__(self):
        return f'[{self.x}, {self.y}, {self.w}, {self.h}]'

    def get_iou_with(self, other: 'Box') -> float:
        return iou(self, other)


def iou(a: Box, b: Box) -> float:
    area_a = a.w * a.h
    area_b = b.w * b.h

    w = min(b.x + b.w, a.x + a.w) - max(a.x, b.x)
    h = min(b.y + b.h, a.y + a.h) - max(a.y, b.y)

    if w <= 0 or h <= 0:
        return 0.0

    area_c = w * h

    return area_c / (area_a + area_b - area_c)


if __name__ == '__main__':
    a = Box(1, 1, 4, 5)
    b1 = Box(1, 1, 4, 5)
    b2 = Box(5, 1, 4, 5)
    b3 = Box(3, 2, 3, 6)

    print("iou ", iou(a, b1))
    print("iou ", iou(a, b2))
    print("iou ", iou(a, b3))
