from typing import Iterable

from reporter.base_reporter import BaseReporter
from reporter.dichotomous.dicho_result import DichoResult
from reporter.util.container import lst, dic
from pyecharts.components import Table


class DichoReporter(BaseReporter):
    def __init__(self):
        self.named_dichos = dic()

    def add(self, name: str, is_res_true: bool, is_exp_true: bool):
        if not isinstance(is_res_true, bool):
            raise Exception('ONLY take "bool" value to prevent mistake from conversion')
        if not isinstance(is_exp_true, bool):
            raise Exception('ONLY take "bool" value to prevent mistake from conversion')
        dicho_result = self.named_dichos.get_or_insert(name, DichoResult(name))
        if is_res_true and is_exp_true:
            dicho_result.tp += 1
        elif is_res_true and not is_exp_true:
            dicho_result.fp += 1
        elif not is_res_true and is_exp_true:
            dicho_result.fn += 1
        elif not is_res_true and not is_exp_true:
            dicho_result.tn += 1

    def build(self):
        pass

    def build_tables(self) -> lst[Table]:
        rtn = lst()
        rtn.append(self.__confusion_matrix_table())
        return rtn

    def __confusion_matrix_table(self) -> Table:
        table = Table()
        table_rows = self.named_dichos.values() \
            .sorted() \
            .map(lambda x: x.dicho_confusion_matrix_table_row())
        headers = ['class', "accuracy", 'TP+TN|TP+TN+FP+FN', "precision", 'TP|TP+FP', 'recall', 'TP|TP+FN',
                   'false positive', 'FP|FP+TN', 'positive expect TP+FN', 'negative expect TN+FP']
        table.add(headers, table_rows)
        return table
