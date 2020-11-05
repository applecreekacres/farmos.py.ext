from datetime import datetime
import mock
from farmer import Farm
from farmer.ext.farmobj import FarmObj, FileFarmObj


@mock.patch("farmer.Farm")
def test_farmobj_empty(mock_farm):
    obj = FarmObj(mock_farm, {})
    assert not obj.name
    assert not obj.images
    assert obj.farm == mock_farm


@mock.patch("farmer.Farm")
def test_farmobj_not_empty(mock_farm):
    obj = FarmObj(mock_farm, {
        "name": "test",
        "images": [
            "image1", "image2"
        ]
    })
    assert obj.name == 'test'
    assert len(obj.images) == 2
    assert obj.farm == mock_farm

@mock.patch("farmer.Farm")
def test_filefarmobj_empty(mock_farm):
    obj = FileFarmObj(mock_farm, {})
    assert not obj.files


@mock.patch("farmer.Farm")
def test_filefarmobj_not_empty(mock_farm):
    obj = FileFarmObj(mock_farm, {
        "name": "filetest",
        "files": ["file1", "file2"]
    })
    assert len(obj.files) == 2
    assert 'filetest' == obj.name


def test_timestamp_to_datetime():
    date = datetime(2020, 6, 26, 5, 4, 34)
    assert date == FarmObj.timestamp_to_datetime(date.timestamp())
    assert not FarmObj.timestamp_to_datetime(None)
