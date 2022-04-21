import dataclasses

from reporter.model.abs.cmp import Comparable
from reporter.model.color_strategy import DEFAULT_PERCENTAGE_COLOR_STRATEGY, DEFAULT_DATA_SIZE_COLOR_STRATEGY, ColorStrategy
from reporter.model.percentage import Percentage
from reporter.model.sum import Sum
from reporter.util.lazy import lazy


class DichoResult(Comparable):

    def __init__(self, name):
        self.name = name
        self.tp = 0
        self.fn = 0
        self.tn = 0
        self.fp = 0
        self.per_cs = DEFAULT_PERCENTAGE_COLOR_STRATEGY
        self.false_pos_cs = ColorStrategy(red=0.10, green=0.05, blue=0.0)
        self.data_cs = DEFAULT_DATA_SIZE_COLOR_STRATEGY

    def dicho_confusion_matrix_table_row(self):
        # accuracy
        acc = self.accuracy
        # precision
        pre = self.precision
        recall = self.recall
        # false positive rate
        fpr = self.fpr
        pos_data = Sum(self.tp, self.fn)
        neg_data = Sum(self.tn, self.fp)
        acc_v, acc_d = self.per_cs.perc_color(acc), self.per_cs.html_color(acc.value, acc.desc)
        pre_v, pre_d = self.per_cs.perc_color(pre), self.per_cs.html_color(pre.value, pre.desc)
        recall_v, recall_d = self.per_cs.perc_color(recall), self.per_cs.html_color(recall.value, recall.desc)
        fpr_v, fpr_d = self.false_pos_cs.perc_color(fpr), self.false_pos_cs.html_color(fpr.value, fpr.desc)
        pos_data_str = self.data_cs.html_color(pos_data)
        neg_data_str = self.data_cs.html_color(neg_data)
        return [self.name, acc_v, acc_d, pre_v, pre_d
            , recall_v, recall_d, fpr_v, fpr_d, pos_data_str, neg_data_str]

    def __str__(self):
        return f'accuracy: {self.accuracy}, precision: {self.precision}, recall: {self.recall}, FPR: {self.fpr}'

    @property
    def fpr(self):
        return Percentage(self.fp, self.fp + self.tn)

    @property
    def accuracy(self):
        return Percentage(self.tp + self.tn, self.tp + self.tn + self.fp + self.fn)

    @property
    def recall(self) -> Percentage:
        return Percentage(self.tp, self.tp + self.fn)

    @property
    def precision(self) -> Percentage:
        return Percentage(self.tp, self.tp + self.fp)

    def __compare_by__(self):
        return self.accuracy
