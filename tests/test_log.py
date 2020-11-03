
from datetime import datetime
from farmer import Farm
from farmer.ext import Log


def test_log_empty():
    log = Log(Farm(), {})
    assert log.id is None


def test_log_data():
    log = Log(Farm(), {
        'id': 5,
        'type': 'farm_activity',
        'timestamp': datetime(2020, 11, 2).timestamp(),
        'done': '0'
    })

    assert log.id == 5
    assert log.type == 'farm_activity'
    assert log.done is False
    assert not log.asset
