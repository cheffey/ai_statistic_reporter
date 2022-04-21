import hashlib

from reporter.util.file_util import Path
from reporter.util.json_util import load_obj, serialize_and_dump

__this_path = Path(__file__)
__CACHE_FOLDER = __this_path.parent().parent().join('cache')


def from_cache(datum_generator, cache_name: str, hash_reference: str):
    cache_folder = __CACHE_FOLDER.join(cache_name)
    if not cache_folder.exists():
        cache_folder.makedirs()
    _hash = to_MD5(hash_reference)
    cache = cache_folder.join(f'{_hash}.json')
    if cache.exists():
        return load_obj(cache)
    result = datum_generator()
    serialize_and_dump(result, cache)
    return result


def to_MD5(string):
    return hashlib.md5(string.encode(encoding='UTF-8')).hexdigest()[:8]


if __name__ == '__main__':
    print(to_MD5('123'))
    print(to_MD5('123'))
    print(to_MD5('123'))
