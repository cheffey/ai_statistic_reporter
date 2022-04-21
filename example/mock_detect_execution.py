from reporter.model.box import Box, ResBox
from reporter.target_detection.detection_reporter import DetectionReporter
from reporter.util.file_util import Path
from reporter.util.json_util import load_obj


# [[82, 31, 185, 247], [249, 0, 321, 148], [334, 0, 383, 94], [414, 0, 453, 54]]
def to_exp_box(exp):
    x = exp[0]
    y = exp[1]
    w = exp[2] - exp[0]
    h = exp[3] - exp[1]
    return Box(x, y, w, h)


# {'left_top': [82, 29], 'right_bottom': [188, 250]}, 'obj_class': 'face', 'obj_score': 0.9594442248344421}
def to_res_box(res) -> ResBox:
    x = res.obj_bbox.left_top[0]
    y = res.obj_bbox.left_top[1]
    w = res.obj_bbox.right_bottom[0] - res.obj_bbox.left_top[0]
    h = res.obj_bbox.right_bottom[1] - res.obj_bbox.left_top[1]
    score = float(res.obj_score)
    return ResBox(x, y, w, h, score)


if __name__ == '__main__':
    reporter = DetectionReporter(min_iou_limit_excluded=0.3)
    mock_data_path = Path(__file__).parent().join('mockdata/detection.json')

    mockdata = load_obj(mock_data_path)
    for datum in mockdata:  # mock each evaluating
        clazz = 'face'
        res_boxes = map(to_res_box, datum['result'])
        exp_boxes = map(to_exp_box, datum['expect'].rects)
        reporter.add(clazz, res_boxes, exp_boxes)

    result = reporter.build_html('mock face test')
