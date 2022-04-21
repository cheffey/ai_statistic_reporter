from reporter.util.data_cache import from_cache


def evaluate(img_path):
    print(f'evaluating ======>>>>>{img_path}')
    return {'result': f'result_of_{img_path}', 'score': 1.0}


def check(res, exp):
    print(f'checking {img_path}')
    return True


if __name__ == '__main__':
    testdata = [{'expect': f'expect{i}', 'img_path': f'img_path{i}'} for i in range(0, 100)]
    for test_datum in testdata:
        exp = test_datum['expect']
        img_path = test_datum['img_path']
        # normal execution:
        # res = evaluate(img_path)
        # use cache, if execution is done before with the same 'cache_name', it would load result from cache instead of evaluating to save time
        res = from_cache(lambda: evaluate(img_path), 'sprint_2', img_path)
        is_success = check(res, exp)
