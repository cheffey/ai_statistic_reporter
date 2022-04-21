import random

from reporter.polytomous.polyto_reporter import PolytoReporter
from reporter.util.container import lst

ANIMAL_TYPES = ['cat', 'dog', 'horse', 'monkey', 'donkey', 'bird', 'fox', 'bear']


def evaluate(expect):
    if random.randint(0, 100) < 92:
        return expect
    else:
        return random.choice(ANIMAL_TYPES)


def random_input(size=1000):
    random.seed(1)
    rtn = lst()
    for i in range(size):
        animal_type = random.choice(ANIMAL_TYPES)
        rtn.append({'expect': animal_type, 'for_evaluation': animal_type})
    return rtn


if __name__ == '__main__':
    reporter = PolytoReporter()
    data = random_input(1000)

    for datum in data:  # mock each evaluating
        expect = datum['expect']
        for_evaluation = datum['for_evaluation']
        result = evaluate(for_evaluation)
        reporter.add('animal_type', result, expect)

        reporter.collect_bool('type matches', result == expect)

    result = reporter.build_html('mock animal type test')
