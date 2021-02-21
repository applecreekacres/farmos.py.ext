
from datetime import datetime

import pytest
from farmos_ext import Farm


@pytest.mark.skip(reason="Need to normalize timezone for testing on CI.")
def test_log():
    farm = Farm()
    log = next(farm.logs(800))

    assert log.id == 800
    assert log.done
    assert log.flags == ['organic']
    assert log.categories[0].name == 'Plantings'
    assert log.created == datetime(2020, 10, 15, 22, 55, 59)
