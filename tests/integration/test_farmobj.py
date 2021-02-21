
from farmos_ext.farm import Farm
from farmos_ext.farmobj import FarmObj


def test_farmobj_creation():
    farm = Farm()
    obj = FarmObj(farm, {'name': 'test'})

    assert obj.name == 'test'
