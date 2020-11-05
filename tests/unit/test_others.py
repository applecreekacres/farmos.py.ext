import mock
from farmer import Farm
from farmer.ext.others import Content, Inventory, Measure, Quantity


def test_quantity():
    quantity = Quantity(Measure('weight'), 'Test', 'Pounds', '34')

    assert quantity.label == 'Test'
    assert quantity.measure == Measure.WEIGHT
    assert quantity.value == '34'
    assert quantity.unit == 'Pounds'

    assert quantity.to_dict() == {
        "measure": 'weight',
        "unit": {
            "name": 'Pounds',
            "resource": 'taxonomy_term'
        },
        "value": '34',
        "label": 'Test'
    }


def test_inventory():
    inventory = Inventory(5, 6)
    assert inventory.asset_id == 6
    assert inventory.value == 5
    assert inventory.to_dict() == {
        "asset": {
            "id": 6
        },
        "value": "5"
    }


@mock.patch("farmer.Farm")
def test_content_empty(mock_farm):
    content = Content(mock_farm, {})
    assert not content.api_version
    assert not content.system_of_measurement
    assert not content.metrics
    assert not content.mapbox_api_key
    assert not content.languages
    assert not content.google_maps_api_key
    assert not content.resources


@mock.patch("farmer.Farm")
def test_content_not_empty(mock_farm):
    content = Content(mock_farm, {
        "api_version": "1.4",
        "system_of_measurement": "us",
        "metrics": {
            "key": "value"
        },
        "mapbox_api_key": "mapbox",
        "languages": {
            "key2": "value2"
        },
        "google_maps_api_key": "google",
        "resources": {
            "key3": "value3"
        }
    })
    assert content.api_version == "1.4"
    assert content.system_of_measurement == "us"
    assert isinstance(content.metrics, dict)
    assert "key" in content.metrics
    assert content.mapbox_api_key == "mapbox"
    assert isinstance(content.languages, dict)
    assert "key2" in content.languages
    assert content.google_maps_api_key == "google"
    assert isinstance(content.resources, dict)
    assert "key3" in content.resources
