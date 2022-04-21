import json
import os.path
from types import SimpleNamespace
from typing import Iterable, Mapping

from reporter.util.container import lst, dic
from reporter.util.file_util import Path


def __load(path):
    with open(str(path), "r", encoding='utf-8') as f:
        json_obj = json.load(f)
    return json_obj


def serialize_and_dump(ori_obj, path):
    json_obj = _serialize(ori_obj)
    with open(str(path), "w", encoding='utf-8') as f:
        json.dump(json_obj, f, ensure_ascii=False)


# load_as_customized_containers
def load_obj(raw_path):
    path = Path(raw_path)
    if not path.exists():
        raise Exception(f'File: {path} NOT exist. ')
    json_obj = __load(path)
    return _use_lst_dic(json_obj)


def _serialize(obj):
    if isinstance(obj, Mapping):
        return dic(obj).map_dic(lambda x, y: _serialize(y))
    if isinstance(obj, str):
        return obj
    if isinstance(obj, Iterable):
        return lst(obj).map(_serialize)
    if hasattr(obj, '__dict__'):
        return _serialize(obj.__dict__)
    obj_type = str(type(obj))
    if obj_type.__contains__('int'):
        return int(obj)
    if obj_type.__contains__('float'):
        return float(obj)
    return obj


def _use_lst_dic(obj):
    if isinstance(obj, dict):
        return dic(obj).map_dic(lambda k, v: _use_lst_dic(v))
    if isinstance(obj, str):
        return obj
    if isinstance(obj, Iterable):
        return lst(obj).map(_use_lst_dic)
    if isinstance(obj, SimpleNamespace):
        return obj
    if hasattr(obj, '__dict__'):
        d = obj.__dict__
        for key in d.keys():
            value = d[key]
            d[key] = _use_lst_dic(value)
    return obj
