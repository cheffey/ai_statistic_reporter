from reporter.model.box import ResBox, Box
from reporter.target_detection.detection_result import DetectionResult
from reporter.util.container import lst, dic


class Detection:
    def __init__(self, res_boxes: lst[ResBox], exp_boxes: lst[Box]):
        self.res_boxes = res_boxes
        self.exp_boxes = exp_boxes
        self.__iou_cache = dic()

    def result(self, score: float, iou_limit: float) -> DetectionResult:
        result_boxes = self.res_boxes.filter(lambda x: x.score >= score)
        found_exp = set()
        found_res = lst()
        for res in result_boxes:
            is_res_found = False
            for exp in self.exp_boxes:
                if self.__iou(res, exp) >= iou_limit:
                    found_exp.add(exp)
                    is_res_found = True
            if is_res_found:
                found_res.append(res)

        exp_gets = len(found_exp)
        exp_targets = len(self.exp_boxes)
        res_tp = len(found_res)
        per_num = len(result_boxes)
        return DetectionResult(exp_gets, exp_targets, res_tp, per_num, score, iou_limit)

    def __iou(self, res_box: ResBox, exp_box: Box):
        res_key = f'{res_box.x},{res_box.y},{res_box.w},{res_box.h}'
        exp_key = f'{exp_box.x},{exp_box.y},{exp_box.w},{exp_box.h}'
        key = res_key + exp_key
        if key not in self.__iou_cache:
            self.__iou_cache[key] = res_box.get_iou_with(exp_box)
        return self.__iou_cache.get(key, None)
