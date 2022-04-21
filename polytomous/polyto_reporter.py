from pyecharts.components import Table

from reporter.base_reporter import BaseReporter
from reporter.polytomous.polyto_result import PolytoResult
from reporter.util.container import lst, dic


class PolytoReporter(BaseReporter):
    def __init__(self):
        self.clazzified_polytos = dic()

    def add(self, clazz: str, res_option: str, exp_option: str):
        if not isinstance(res_option, str):
            raise Exception(f'option ONLY take "str" to prevent mistake from conversion')
        if not isinstance(exp_option, str):
            raise Exception(f'option ONLY take "str" to prevent mistake from conversion')
        polyto_result = self.clazzified_polytos.get_or_insert(clazz, PolytoResult(clazz))
        polyto_result.add(res_option, exp_option)

    def build(self):
        pass

    def build_tables(self) -> lst[Table]:
        tables = lst()
        for polyto_res in self.clazzified_polytos.values():
            tables.append(polyto_res.build_table())
            tables.append(polyto_res.build_mismatch_bar())
        return tables
