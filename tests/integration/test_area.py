
from farmer import Farm


def test_area():
    farm = Farm()
    area = next(farm.areas(251))

    assert area.tid == 251
    assert area.flags == ['review', 'organic']
    assert area.name == 'High Tunnel'
