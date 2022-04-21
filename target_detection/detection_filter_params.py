import dataclasses

from reporter.util.container import lst


@dataclasses.dataclass
class DetFilParams:
    min_score_excluded: float
    max_score_excluded: float
    min_iou_limit_excluded: float
    max_iou_limit_excluded: float

    def __post_init__(self):
        assert self.min_score_excluded >= 0 and self.min_score_excluded <= 1
        assert self.max_score_excluded >= 0 and self.max_score_excluded <= 1
        assert self.min_iou_limit_excluded >= 0 and self.min_iou_limit_excluded <= 1
        assert self.max_iou_limit_excluded >= 0 and self.max_iou_limit_excluded <= 1

    def score_range(self):
        per_step = 10  # todo
        min_per_excluded = int(self.min_score_excluded * 100)
        max_per_excluded = int(self.max_score_excluded * 100)
        r = lst(range(min_per_excluded, max_per_excluded, per_step))
        per_range = r[1:]
        return per_range.map(lambda x: x / 100)

    def iou_limit_range(self):
        per_step = 10  # todo
        min_per_excluded = int(self.min_iou_limit_excluded * 100)
        max_per_excluded = int(self.max_iou_limit_excluded * 100)
        r = lst(range(min_per_excluded, max_per_excluded, per_step))
        per_range = r[1:]
        return per_range.map(lambda x: x / 100)


if __name__ == '__main__':
    params = DetFilParams(0, 1, 0, 1)
    score_range = params.score_range()
    print()
