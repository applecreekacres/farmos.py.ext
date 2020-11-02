
from farmer.ext.asset import Asset
from farmer.ext.farm import Farm
from farmer.ext.farmobj import FarmObj


def test_farmobj_creation():
    farm = Farm()
    obj = FarmObj(farm, {'name': 'test'})

    assert obj.name == 'test'
