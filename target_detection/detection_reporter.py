from typing import Iterable

import pyecharts.options as opts
from pyecharts.charts import Line
from pyecharts.components import Table

from reporter.base_reporter import BaseReporter
from reporter.model.box import ResBox, Box
from reporter.model.percentage import Percentage
from reporter.target_detection.detection import Detection
from reporter.target_detection.detection_filter_params import DetFilParams
from reporter.target_detection.detection_result import DetectionResult
from reporter.util.container import lst, dic

_AP_CURVE_COLORS = lst.of('blue', 'green', 'purple', 'yellow', 'red')


class DetectionReporter(BaseReporter):
    def __init__(self, min_score_excluded=0.0, max_score_excluded=1.0
                 , min_iou_limit_excluded=0.0, max_iou_limit_excluded=1.0):
        self.classed_detections = dic()
        self.params = DetFilParams(min_score_excluded, max_score_excluded, min_iou_limit_excluded, max_iou_limit_excluded)

    def add(self, clazz: str, res_boxes: Iterable[ResBox], exp_boxes: Iterable[Box]):
        detections = self.classed_detections.get_or_insert(clazz, lst())
        detections.append(Detection(lst(res_boxes), lst(exp_boxes)))

    def build(self):
        det_sums = dic()
        for clazz, detections, in self.classed_detections.pairs():
            det_results: lst[DetectionResult] = _get_det_results(detections, self.params)
            det_sum: lst[DetectionResult] = _get_top_10(det_results)
            det_sums[clazz] = det_sum
        return det_sums

    def build_tables(self) -> lst[Table]:
        rtn = lst()
        for clazz, detections, in self.classed_detections.pairs():
            det_results: lst[DetectionResult] = _get_det_results(detections, self.params)
            det_sum: lst[DetectionResult] = _get_top_10(det_results)
            rtn.append(self.__build_table(clazz, det_sum))
            iou_det = det_results.group_by(lambda x: x.iou_limit)
            iou_AP_det = iou_det.map_lst(lambda iou, det: (iou, _calc_AP(det), det)).sorted(key=lambda x: x[1], reverse=True)
            for i, (iou, AP, det) in enumerate(iou_AP_det):
                color = _AP_CURVE_COLORS.get(i, 'black')
                rtn.append(self.__build_PR_chart(iou, AP, det, color))
        return rtn

    def __build_table(self, clazz: str, det_sum: lst[DetectionResult]) -> Table:
        table_rows = det_sum.map(lambda x: x.target_detection_table_row(clazz))
        table = Table()
        headers = ['class', "precision", '[correct|result size]', 'recall', '[detected|expect size]', '[result size|expect size]', 'F1']
        table.add(headers, table_rows)
        return table

    def __build_PR_chart(self, iou, AP: Percentage, det: lst[DetectionResult], color="red"):
        recall_as_x, precision_as_y = det.split(lambda x: round(x.recall.value, 2), lambda x: round(x.precision.value, 2))
        line = Line().set_global_opts(
            tooltip_opts=opts.TooltipOpts(is_show=False),
            xaxis_opts=opts.AxisOpts(type_="value", min_=recall_as_x.min(), max_=recall_as_x.max()),
            yaxis_opts=opts.AxisOpts(type_="value", min_=precision_as_y.min(), max_=precision_as_y.max()))
        line.add_xaxis(xaxis_data=recall_as_x)
        line.add_yaxis(series_name=f'AP: {AP.value_str}, IOU: {iou}', y_axis=precision_as_y, linestyle_opts=opts.LineStyleOpts(color=color, width=2))
        return line


def _get_det_results(detections, params: DetFilParams) -> lst[DetectionResult]:
    det_results = lst()
    for score in params.score_range():
        for iou_limit in params.iou_limit_range():
            det_result = detections.map(lambda x: x.result(score, iou_limit)) \
                .reduce(lambda a, b: a + b, None)
            if det_result is not None:
                det_results.append(det_result)
    return det_results


def _get_top_10(det_results: lst[DetectionResult]) -> lst[DetectionResult]:
    top_10_results = lst()
    for det_result in det_results:
        top_10_results = _update_top10_results(top_10_results, det_result)
    return top_10_results


def _update_top10_results(top_10_results: lst[DetectionResult], det_result: DetectionResult):
    top_10_results.sort(reverse=True)
    for i in range(0, len(top_10_results)):
        other = top_10_results[i]
        if det_result == other:
            if det_result.score + det_result.iou_limit > other.score + other.iou_limit:
                top_10_results[i] = det_result
                return top_10_results
        if det_result > other:
            top_10_results.insert(i, det_result)
            return top_10_results[:10]
    top_10_results.append(det_result)
    return top_10_results[:10]


def _calc_AP(det: lst[DetectionResult]):
    p_r_pair = det.map(lambda x: (x.precision, x.recall))
    recalls = p_r_pair.map(lambda x: x[1]).without_duplicate().sorted()
    last_r = 0
    total_area = 0
    for r_percentage in recalls:
        r = r_percentage.value
        p_max = p_r_pair.filter(lambda x: x[1] == r).map(lambda x: x[0]).max().value
        area = (r - last_r) * p_max
        total_area += area
        last_r = r
    return Percentage(total_area)
