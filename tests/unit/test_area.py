import mock
from mock.mock import MagicMock

from farmer.area import Area


@mock.patch("farmer.Farm")
def test_area_empty(mock_farm: MagicMock):
    mock_farm.assets.return_value = []
    mock_farm.areas.return_value = []
    area = Area(mock_farm, {})

    assert not area.tid
    assert not area.description
    assert not area.flags
    assert not area.geofield
    assert not area.vocabulary
    assert not area.parent
    mock_farm.areas.assert_called_with(None)
    assert not area.parents_all
    mock_farm.areas.assert_called_with(None)
    assert not area.assets
    mock_farm.assets.assert_called_with(None)


@mock.patch("farmer.Farm")
def test_area_not_empty(mock_farm: MagicMock):
    area = Area(mock_farm, {
        "tid": '4',
        "description": 'small description',
        'flags': ['flag1', 'flag2', 'flag3'],
        "geofield": 'well-known text',
        "vocabulary": {
            "key": "value"
        },
        "parent": [
            {
                "parent": "value"
            }
        ],
        "parents_all": [
            {
                "parent2":  "value2"
            },
            {
                "parent3": "value3"
            }
        ],
        "assets": [
            {"asset": "5"}
        ]
    })

    assert area.tid == 4
    assert area.description == "small description"
    assert len(area.flags) == 3
    assert area.geofield == "well-known text"
    assert isinstance(area.vocabulary, dict)
    assert "key" in area.vocabulary

    area.parent
    mock_farm.areas.assert_called_with([{"parent": "value"}])

    area.parents_all
    mock_farm.areas.assert_called_with([
        {
            "parent2":  "value2"
        },
        {
            "parent3": "value3"
        }
    ])

    area.assets
    mock_farm.assets.assert_called_with([
        {"asset": "5"}
    ])
