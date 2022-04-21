import os

from reporter.util.container import lst


class Path(os.PathLike):
    def __init__(self, value):
        if isinstance(value, Path):
            self.__value = value.__value
        else:
            self.__value = str(value)
        self.basename = os.path.basename(value)

    def __fspath__(self):
        return os.path.abspath(self.__value).replace('\\', '/')

    def join(self, *extensions) -> 'Path':
        for sub_path in extensions:
            if not sub_path:
                raise Exception(f'sub_path can NOT be empty: {sub_path}')
        return Path(os.path.join(self.__value, *extensions))

    def makedirs(self):
        os.makedirs(self.__value)

    def exists(self) -> bool:
        return os.path.exists(self.__value)

    def files(self) -> 'lst[Path]':
        return lst(os.listdir(self.__value)).map(lambda x: self.join(x))

    def __str__(self):
        return self.__fspath__()

    def parent(self) -> 'Path':
        return Path(os.path.dirname(self))
