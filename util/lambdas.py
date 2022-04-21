from typing import Callable
from typing import Type

X = Type['X']
combine: Callable[[X, X], X] = lambda x, y: x + y
