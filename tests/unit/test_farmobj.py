from datetime import datetime

import mock
from farmer import Farm
from farmer.ext.farmobj import FarmObj


@mock.patch("farmer.Farm")
def test_farmobj_empty(mock_farm):
    obj = FarmObj(mock_farm, {})
    assert not obj.name
    assert obj.farm == mock_farm


@mock.patch("farmer.Farm")
def test_farmobj_not_empty(mock_farm):
    obj = FarmObj(mock_farm, {
        "name": "test",
    })
    assert obj.name == 'test'
    assert obj.farm == mock_farm
