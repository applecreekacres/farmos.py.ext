
from farmer.farm import Farm
from farmer.farmobj import FarmObj


def test_farmobj_creation():
    farm = Farm()
    obj = FarmObj(farm, {'name': 'test'})

    assert obj.name == 'test'
