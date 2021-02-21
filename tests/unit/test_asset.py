from datetime import date, datetime
from farmos_ext.term import Crop, Season
import mock
from mock.mock import MagicMock

from farmos_ext.asset import Asset, Planting


@mock.patch("farmos_ext.Farm")
def test_asset_empty(mock_farm: MagicMock):

    asset = Asset(mock_farm, {})
    assert not asset.archived

    assert not asset.created
    assert not asset.description
    assert not asset.name
    assert not asset.id
    assert not asset.type
    assert not asset.flags
    assert not asset.uid
    assert not asset.data
    assert not asset.changed


@mock.patch("farmos_ext.Farm")
def test_asset_complete(mock_farm: MagicMock):
    created = datetime.now()
    changed = datetime(2020, 11, 8, 4, 29, 45)
    archived = datetime(2020, 11, 8, 4, 35, 23)
    asset = Asset(mock_farm, {
        "created": int(created.timestamp()),
        "name": "Test Asset",
        "description": "Test description",
        "data": "{}",
        "flags": ['a', 'b'],
        "changed": int(changed.timestamp()),
        "type": "planting",
        "uid": '56',
        'archived': int(archived.timestamp())
    })

    # Don't care below seconds so make it an int of the timestamp
    assert int(asset.created.timestamp()) == int(created.timestamp())
    assert asset.name == "Test Asset"
    assert asset.description == "Test description"
    assert asset.data == "{}"
    assert asset.flags == ['a', 'b']
    assert asset.changed.timestamp() == changed.timestamp()
    assert asset.type == "planting"
    assert asset.uid == 56
    assert asset.archived.timestamp() == archived.timestamp()


@mock.patch("farmos_ext.Farm")
def test_planting_empty(mock_farm:  MagicMock):
    mock_farm.terms.return_value = []
    planting = Planting(mock_farm, {})

    assert not planting.season
    mock_farm.terms.assert_called_with(None, Season)
    assert not planting.crop
    assert mock_farm.terms.call_count == 2
    mock_farm.terms.assert_called_with(None, Crop)


@mock.patch("farmos_ext.Farm")
def test_planting_data(mock_farm: MagicMock):

    planting = Planting(mock_farm, {
        "crop": [{}],
        "season": [{}]
    })

    mock_farm.terms.return_value = Crop(mock_farm, {})
    assert isinstance(planting.crop, Crop)
    mock_farm.terms.assert_called_with([{}], Crop)
    mock_farm.terms.return_value = Season(mock_farm, {})
    assert isinstance(planting.season, Season)
    mock_farm.terms.assert_called_with([{}], Season)
    assert mock_farm.terms.call_count == 2
