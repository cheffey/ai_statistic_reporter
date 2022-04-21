import abc
import os
import sys
from typing import List

from pyecharts.charts import Page
from pyecharts.charts.mixins import ChartMixin
from pyecharts.render.engine import write_utf8_html_file

from reporter.bool_collector import BoolCollector
from reporter.util.container import lst, dic

bool_collectors = dic()


class BaseReporter(metaclass=abc.ABCMeta):

    def collect_bool(self, switch_name, is_true: bool):
        if not isinstance(is_true, bool):
            raise Exception('ONLY take "bool" value to prevent mistake from conversion')
        bool_col = bool_collectors.get_or_insert(switch_name, BoolCollector(switch_name))
        bool_col.add(is_true)

    @abc.abstractmethod
    def build_tables(self) -> lst[ChartMixin]:
        pass

    def build_html(self, title, path=None):
        html_str = self.__build_html_str(title)
        if path is None:
            path = f'{title}_stat.html'
        write_utf8_html_file(path, html_str)
        if sys.platform == 'win32':
            os.startfile(path)

    def __build_html_str(self, title):
        page = Page()
        page.page_title = title
        page.add(*self.__tables())
        html_str = _remove_escapes(page)
        return html_str

    def __tables(self) -> lst[ChartMixin]:
        rtn = lst()
        if bool_collectors:
            bool_col_table = BoolCollector.build_table(bool_collectors.values())
            rtn.append(bool_col_table)
        for chart in self.build_tables():
            if isinstance(chart, ChartMixin):
                rtn.append(chart)
            elif isinstance(chart, List):
                rtn.extend(chart)
            else:
                raise Exception(f'unknown chart type: {type(chart)}')
        return rtn


def _remove_escapes(page):
    html_str = page.render_embed()
    html_after_rep = html_str \
        .replace('&quot;', '"') \
        .replace('&lt;', '<') \
        .replace('&gt;', '>')
    return html_after_rep
