from reporter.model.abs.cmp import Comparable
from reporter.model.color_strategy import DEFAULT_PERCENTAGE_COLOR_STRATEGY, DEFAULT_DATA_SIZE_COLOR_STRATEGY
from reporter.model.percentage import Percentage


class PolytoOptionResult(Comparable):
    def __init__(self, option_name):
        self.option_name = option_name
        self.tp = 0
        self.fp = 0
        self.fn = 0
        self.per_cs = DEFAULT_PERCENTAGE_COLOR_STRATEGY
        self.data_cs = DEFAULT_DATA_SIZE_COLOR_STRATEGY

    def __compare_by__(self):
        return self.F1

    @property
    def precision(self) -> Percentage:
        return Percentage(self.tp, self.tp + self.fp)

    @property
    def recall(self) -> Percentage:
        return Percentage(self.tp, self.tp + self.fn)

    @property
    def F1(self) -> float:
        if self.recall.is_division_by_zero() or self.precision.is_division_by_zero():
            return -1
        recall = self.recall.value
        pre = self.precision.value
        if recall == 0:
            return 0
        return 2 * recall * pre / (recall + pre)

    def polyto_confusion_matrix_table_row(self):
        # precision
        pre = self.precision
        recall = self.recall
        # false positive rate
        tp_fp_fn = f'{self.tp}|{self.fp}|{self.fn}'
        pre_v, pre_d = self.per_cs.perc_color(pre), self.per_cs.html_color(pre.value, pre.desc)
        recall_v, recall_d = self.per_cs.perc_color(recall), self.per_cs.html_color(recall.value, pre.desc)
        data_size = self.data_cs.html_color(self.tp + self.fn)
        return [self.option_name, pre_v, pre_d, recall_v, recall_d
            , data_size, tp_fp_fn, self.F1]

    def __str__(self):
        return f'precision: {self.precision}, recall: {self.recall}, F1: {self.F1}'
