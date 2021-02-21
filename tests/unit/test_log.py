
from datetime import datetime
from farmer.area import Area
from farmer.asset import Asset, Equipment
from mock import patch
from mock.mock import MagicMock
from farmer.log import Log


@patch("farmer.Farm")
def test_log_empty(mock_farm: MagicMock):
    log = Log(mock_farm, {})

    assert not log.type
    assert not log.timestamp
    assert not log.done
    assert not log.notes
    assert not log.asset
    assert not log.equipment
    assert not log.area
    assert not log.geofield
    assert not log.movement
    assert not log.membership
    assert not log.quantity
    assert not log.flags
    assert not log.categories
    assert not log.owner
    assert not log.created
    assert not log.changed
    assert not log.uid
    assert not log.data
    assert not log.inventory


@patch("farmer.Farm")
def test_log_data(mock_farm: MagicMock):
    timstamp = datetime.now()
    created = datetime(2020, 11, 9, 6, 44, 23)
    changed = datetime(2015, 4, 16, 10, 34, 45)
    data = {
        "type": "farm_activity",
        "timestamp": int(timstamp.timestamp()),
        "done": '0',
        "notes": {
            "value": "Test Note"
        },
        "asset": [{"asset": "test"}],
        "equipment": [{"equipment": "test"}],
        "area": [{"area": "test"}],
        "geofield": "well known text",
        "movement": {"area": "test"},
        "membership": "member",
        "quantity": [{
            "measure": "count",
            "label": "quantity test",
            "value": "56",
            "unit": 'Plants'
        }],
        "flags": ["organic"],
        "log_category": ["plantings"],
        "log_owner": "Me",
        "created": int(created.timestamp()),
        "changed": int(changed.timestamp()),
        "uid": "32453453",
        "data": "This is anything",
        "inventory": [{
            "value": "87",
            "asset": {
                "id": "15"
            }
        }]
    }

    log = Log(mock_farm, data)

    assert log.type == data['type']
    assert log.timestamp.timestamp() == data['timestamp']
    assert not log.done
    assert log.notes == data['notes']['value']

    mock_farm.assets.return_value = [Asset(mock_farm, {})]
    assert isinstance(log.asset[0], Asset)
    mock_farm.assets.assert_called_with(data['asset'], Asset)

    mock_farm.assets.return_value = [Equipment(mock_farm, {})]
    assert isinstance(log.equipment[0], Equipment)
    mock_farm.assets.assert_called_with(data['equipment'], Equipment)

    mock_farm.areas.return_value = [Area(mock_farm, {})]

    assert isinstance(log.area[0], Area)
    mock_farm.areas.assert_called_with(data['area'], Area)

    assert log.geofield == data['geofield']
    mock_farm.areas.return_value = [Area(mock_farm, {})]
    assert isinstance(log.movement[0], Area)
    mock_farm.areas.assert_called_with(data['movement']['area'], Area)

    assert log.membership == data['membership']

    assert len(log.quantity) == 1
    assert log.quantity[0].measure == data['quantity'][0]['measure']

    assert log.flags == data['flags']
    # assert log.categories[0] == data['log_category'][0]
    assert log.owner == data['log_owner']
    assert log.created.timestamp() == data['created']
    assert log.changed.timestamp() == data['changed']
    assert log.uid == int(data['uid'])
    assert log.data == data['data']
    assert len(log.inventory) == 1
    assert log.inventory[0].asset_id == data['inventory'][0]['asset']['id']
