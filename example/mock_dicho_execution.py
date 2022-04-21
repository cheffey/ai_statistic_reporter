from reporter.dichotomous.dicho_reporter import DichoReporter
from reporter.util.file_util import Path
from reporter.util.json_util import load_obj

ATT_NAMES = ['is_male', 'is_coder', 'is_bald', 'wear_plaid_shirt', 'is_asian', 'is_on_phone', 'wearing_slipper', 'is_married',
             'on_bluetooth']


def to_bool(obj):
    if obj in ['True', 'true', True]:
        return True
    if obj in ['False', 'false', False]:
        return False
    else:
        raise Exception(f'')


if __name__ == '__main__':
    reporter = DichoReporter()
    mock_data_path = Path(__file__).parent().join('mockdata/dicho.json')

    mockdata = load_obj(mock_data_path)
    for datum in mockdata:  # mock each evaluating
        # {"is_male": {"name": "False", "score": 0.9998642206192017}, "is_coder": {"name": "False", "score": 0.9986715316772461}, "is_bald": {"name": "False", "score": 0.9998786449432373}, "wear_plaid_shirt": {"name": "False", "score": 0.999445378780365}, "is_asian": {"name": "False", "score": 0.9999642372131348}, "is_on_phone": {"name": "False", "score": 0.999893307685852}, "wearing_slipper": {"name": "True", "score": 0.747269868850708}, "is_married": {"name": "False", "score": 0.9836910367012024}, "on_bluetooth": {"name": "False", "score": 0.9999438524246216}}
        res = datum['result']
        # {"is_male": false, "is_coder": false, "is_bald": false, "wear_plaid_shirt": false, "is_asian": false, "is_on_phone": false, "wearing_slipper": true, "is_married": false, "on_bluetooth": false, "img_path": "image/jc_sjt_mix_0017.jpg", "id": 17}
        exp = datum['expect']
        for att_name in ATT_NAMES:
            is_res_true = to_bool(res[att_name]['name'])
            is_exp_true = to_bool(exp[att_name])
            # ONLY take "bool" value to prevent mistake from conversion
            reporter.add(att_name, is_res_true, is_exp_true)

    result = reporter.build_html('mock human attribute test')
