"""General FarmOS Asset."""

from __future__ import annotations

from datetime import datetime
from typing import Dict, List, Union

from farmer.ext.farmobj import FarmObj
from farmer.ext.term import Crop


class Asset(FarmObj):

    def __init__(self, farm, keys):
        if 'resource' not in keys:
            super(Asset, self).__init__(farm, keys)
        elif 'resource' in keys and keys['resource'] == 'farm_asset':
            super(Asset, self).__init__(
                farm, farm.asset.get({'id': keys['id']})['list'][0])

    @property
    def id(self) -> str:
        return FarmObj._basic_prop(self._keys['id'])

    @property
    def type(self) -> str:
        return FarmObj._basic_prop(self._keys['type'])

    @property
    def description(self) -> Dict:
        return FarmObj._basic_prop(self._keys['description'])

    @property
    def archived(self) -> Union[datetime, None]:
        if self._keys != '0':
            return FarmObj._ts_to_dt(self._keys['archived'])
        else:
            return None

    @property
    def images(self) -> List:
        return FarmObj._basic_prop(self._keys['images'])

    @property
    def files(self) -> List:
        return FarmObj._basic_prop(self._keys['files'])

    @property
    def flags(self) -> List[str]:
        return FarmObj._basic_prop(self._keys['flags'])

    @property
    def created(self) -> Union[datetime, None]:
        return FarmObj._ts_to_dt(self._keys['created'])

    @property
    def changed(self) -> Union[datetime, None]:
        return FarmObj._ts_to_dt(self._keys['changed'])

    @property
    def uid(self) -> Union[int, None]:
        return int(self._keys['uid']) if self._keys['uid'] else None

    @property
    def data(self) -> str:
        return FarmObj._basic_prop(self._keys['data'])


class Planting(Asset):

    @property
    def crop(self) -> List[Crop]:
        return self._get_terms(self._keys['crop'], Crop)


class Animal(Asset):

    @property
    def animal_type(self) -> str:
        return FarmObj._basic_prop(self._keys['animal_type'])

    @property
    def nicknames(self) -> List[str]:
        return FarmObj._basic_prop(self._keys['animal_nicknames'])

    @property
    def castrated(self) -> bool:
        return FarmObj._basic_prop(self._keys['animal_castrated'])

    @property
    def sex(self) -> str:
        return FarmObj._basic_prop(self._keys['animal_sex'])

    @property
    def tag(self):
        return FarmObj._basic_prop(self._keys['tag'])

    @property
    def parent(self) -> List[Animal]:
        return self._get_assets(self._keys['parent'], Animal)

    @property
    def birth_date(self) -> Union[datetime, None]:
        return FarmObj._ts_to_dt(self._keys['date'])


class Equipment(Asset):

    @property
    def manufacturer(self) -> str:
        return FarmObj._basic_prop(self._keys['manufacturer'])

    @property
    def model(self) -> str:
        return FarmObj._basic_prop(self._keys['model'])

    @property
    def serial_number(self) -> str:
        return FarmObj._basic_prop(self._keys['serial_number'])
