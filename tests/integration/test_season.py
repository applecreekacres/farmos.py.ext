
from farmos_ext.farm import Farm


def test_season():
    farm = Farm()
    seasons = [season for season in farm.seasons]
    assert len(seasons) > 0
    assert hasattr(seasons[0], "name")
