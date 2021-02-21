from datetime import datetime

import mock
from farmos_ext import Farm
from farmos_ext.farmobj import FarmObj


@mock.patch("farmos_ext.Farm")
def test_farmobj_empty(mock_farm):
    obj = FarmObj(mock_farm, {})
    assert not obj.name
    assert obj.farm == mock_farm


@mock.patch("farmos_ext.Farm")
def test_farmobj_not_empty(mock_farm):
    obj = FarmObj(mock_farm, {
        "name": "test",
    })
    assert obj.name == 'test'
    assert obj.farm == mock_farm
