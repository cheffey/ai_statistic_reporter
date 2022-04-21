from typing import TypeVar, Callable

from reporter.util.container import lst

X = TypeVar('X')


class TopRankContainer:
    def __init__(self, limit: int, comparator: Callable[[X], object] = lambda x: x):

        self.__elements = lst()
        self.limit = limit
        self.comparator = comparator

    def add(self, element: X):
        if len(self.__elements) >= self.limit:
            self.__elements[0] = element
        else:
            self.__elements.append(element)
        self.__elements.sort(key=self.comparator)


if __name__ == '__main__':
    container = TopRankContainer(10)
    for i in range(1, 100):
        container.add(i)
    print()
