"""General FarmOS Asset."""

from __future__ import annotations

from datetime import datetime
from typing import Dict, List, Union

from farmer.ext.farmobj import FarmObj
from farmer.ext.term import Crop


class Asset(FarmObj):

    def __init__(self, farm, keys):
        if 'resource' not in keys:
            super().__init__(farm, keys)
        elif 'resource' in keys and keys['resource'] == 'farm_asset':
            super().__init__(
                farm, farm.asset.get({'id': keys['id']})['list'][0])

    @property
    def id(self) -> str:  # pylint: disable=invalid-name
        return self._attr('id', str)

    @property
    def type(self) -> str:
        return self._attr('type', str)

    @property
    def description(self) -> Dict:
        return self._attr('description', str)

    @property
    def archived(self) -> Union[datetime, None]:
        if self._keys != '0':
            return FarmObj.timestamp_to_datetime(self._keys['archived'])
        else:
            return None

    @property
    def flags(self) -> List[str]:
        return self._attr('flags', str)

    @property
    def created(self) -> Union[datetime, None]:
        return FarmObj.timestamp_to_datetime(self._keys['created'])

    @property
    def changed(self) -> Union[datetime, None]:
        return FarmObj.timestamp_to_datetime(self._keys['changed'])

    @property
    def uid(self) -> Union[int, None]:
        return int(self._keys['uid']) if self._keys['uid'] else None

    @property
    def data(self) -> str:
        return self._attr('data', str)


class Planting(Asset):

    @property
    def crop(self) -> List[Crop]:
        return self._get_terms(self._keys['crop'], Crop)

    @property
    def season(self):
        return None


class Animal(Asset):

    @property
    def animal_type(self) -> str:
        return self._attr('animal_type', str)

    @property
    def nicknames(self) -> List[str]:
        return self._attr('animal_nicknames', list)

    @property
    def castrated(self) -> bool:
        return self._attr('animal_castrated', bool)

    @property
    def sex(self) -> str:
        return self._attr('animal_sex', str)

    @property
    def tag(self):
        return self._attr('tag', str)

    @property
    def parent(self) -> List[Animal]:
        return self._get_assets(self._keys['parent'], Animal)

    @property
    def birth_date(self) -> Union[datetime, None]:
        return FarmObj.timestamp_to_datetime(self._keys['date'])


class Equipment(Asset):

    @property
    def manufacturer(self) -> str:
        return self._attr('manufacturer', str)

    @property
    def model(self) -> str:
        return self._attr('model', str)

    @property
    def serial_number(self) -> str:
        return self._attr('serial_number', str)


class Sensor(Asset):
    pass


class Compost(Asset):
    pass
