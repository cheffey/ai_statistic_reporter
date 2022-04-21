from typing import Iterable

from pyecharts.components import Table

from reporter.model.color_strategy import DEFAULT_PERCENTAGE_COLOR_STRATEGY, DEFAULT_DATA_SIZE_COLOR_STRATEGY
from reporter.model.percentage import Percentage
from reporter.util.container import lst

per_cs = DEFAULT_PERCENTAGE_COLOR_STRATEGY
data_cs = DEFAULT_DATA_SIZE_COLOR_STRATEGY


class BoolCollector:
    @staticmethod
    def build_table(bool_cols: Iterable['BoolCollector']) -> Table:
        table = Table()
        headers = ['name', "true", 'false', 'total', 'true rate']
        rows = lst()
        for bool_col in bool_cols:
            true_per: Percentage = bool_col.true_percentage()
            colored_true_per = per_cs.html_color(true_per, true_per)
            rows.append((bool_col.name, bool_col.true_cnt, bool_col.false_cnt,
                         bool_col.true_cnt + bool_col.false_cnt, colored_true_per))
        table.add(headers, rows)
        return table

    def __init__(self, name: str):
        self.name = name
        self.true_cnt = 0
        self.false_cnt = 0

    def true_percentage(self) -> Percentage:
        return Percentage(self.true_cnt, self.true_cnt + self.false_cnt)

    def add(self, value: bool):
        if not isinstance(value, bool):
            raise Exception('ONLY take "bool" value to prevent mistake from conversion')
        if value:
            self.true_cnt += 1
        else:
            self.false_cnt += 1
