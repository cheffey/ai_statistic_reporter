from reporter.model.abs.cmp import Comparable
from reporter.model.color_strategy import DEFAULT_PERCENTAGE_COLOR_STRATEGY, DEFAULT_DATA_SIZE_COLOR_STRATEGY
from reporter.model.percentage import Percentage


class DetectionResult(Comparable):

    def __init__(self, exp_gets: int, exp_targets: int,
                 res_tp: int, res_pre_num: int,
                 score: float, iou_limit: float):
        self.exp_gets = exp_gets
        self.exp_targets = exp_targets
        self.res_tp = res_tp
        self.res_pre_num = res_pre_num
        self.score = score
        self.iou_limit = iou_limit
        self.per_cs = DEFAULT_PERCENTAGE_COLOR_STRATEGY
        self.data_cs = DEFAULT_DATA_SIZE_COLOR_STRATEGY

    def target_detection_table_row(self, clazz: str):
        name = f'{clazz}(score: {self.score}, IOU: {self.iou_limit})'
        tp_pre_num = f'{self.res_tp}|{self.res_pre_num}'
        gets_targets = f'{self.exp_gets}|{self.exp_targets}'
        res_exp_size = f'{self.res_pre_num}|{self.exp_targets}'

        return [name, self.per_cs.html_color(self.precision), tp_pre_num,
                self.per_cs.html_color(self.recall), gets_targets, res_exp_size, self.per_cs.html_color(self.F1)]

    def __str__(self):
        return f'score: {self.score}, iou_limit: {self.iou_limit}' \
               f', precision: {self.precision}, recall: {self.recall}, F1: {self.F1}'

    @property
    def recall(self) -> Percentage:
        return Percentage(self.exp_gets, self.exp_targets)

    @property
    def precision(self) -> Percentage:
        return Percentage(self.res_tp, self.res_pre_num)

    @property
    def F1(self) -> float:
        if self.recall.is_division_by_zero() or self.precision.is_division_by_zero():
            return -1
        recall = self.recall.value
        pre = self.precision.value
        return 2 * recall * pre / (recall + pre)

    def __add__(self, other):
        assert isinstance(other, DetectionResult)
        return DetectionResult(self.exp_gets + other.exp_gets,
                               self.exp_targets + other.exp_targets,
                               self.res_tp + other.res_tp,
                               self.res_pre_num + other.res_pre_num,
                               self.score, self.iou_limit)

    def __compare_by__(self):
        return self.F1
