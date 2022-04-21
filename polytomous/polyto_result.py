from pyecharts import options as opts
from pyecharts.charts import Bar
from pyecharts.components import Table

from reporter.polytomous.polyto_option_result import PolytoOptionResult
from reporter.util.container import dic


class PolytoResult:

    def __init__(self, clazz):
        self.clazz = clazz
        self.correct_cnt = 0
        self.wrong_cnt = 0
        self.option_results = dic()
        self.mismatches = dic()

    def build_table(self) -> Table:
        table = Table()
        table_rows = self.option_results.values() \
            .sorted() \
            .map(lambda x: x.polyto_confusion_matrix_table_row())
        headers = [self.clazz, "precision", '[TP|TP+FP]', 'recall', '[TP|TP+FN]', 'data size', 'TP|FP|FN', "F1"]
        table.add(headers, table_rows)
        return table

    def build_mismatch_bar(self) -> Bar:
        bar = Bar()
        sorted_mismatch_count = self.mismatches.pairs().sorted(key=lambda x: x[1])
        mismatch_desc = sorted_mismatch_count.map(lambda x: x[0])
        counts = sorted_mismatch_count.map(lambda x: x[1])
        bar.set_global_opts(title_opts=opts.TitleOpts(title=f'{self.clazz} mismatch count'))
        bar.add_xaxis(xaxis_data=mismatch_desc)
        bar.add_yaxis('mismatch count', y_axis=counts, color='blue')
        bar.set_series_opts(label_opts=opts.LabelOpts(position="right"))
        bar.reversal_axis()
        return bar

    def add(self, res_option, exp_option):
        res_opt_results = self.option_results.get_or_insert(res_option, PolytoOptionResult(res_option))
        exp_opt_results = self.option_results.get_or_insert(exp_option, PolytoOptionResult(exp_option))
        if res_option == exp_option:
            res_opt_results.tp += 1
        else:
            res_opt_results.fp += 1
            exp_opt_results.fn += 1
            mismatch_desc = f'{res_option} exp: {exp_option}'
            self.mismatches[mismatch_desc] = self.mismatches.get(mismatch_desc, 0) + 1
