
from farmer.ext.farm import Farm

def test_farm_content():
    farm = Farm()
    assert farm.content.api_version is not None
    assert farm.content.google_maps_api_key is not None
    assert farm.content.mapbox_api_key is not None
    assert farm.content.name is not None
