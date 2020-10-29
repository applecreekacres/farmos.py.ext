
from datetime import datetime
from typing import Dict, List

from farmer.ext.farmobj import FarmObj
from farmer.ext.term import Crop


class Asset(FarmObj):

    def __init__(self, farm, keys):
        if 'resource' not in keys:
            super(Asset, self).__init__(farm, keys)
        elif 'resource' in keys and keys['resource'] == 'farm_asset':
            super(Asset, self).__init__(farm, farm.asset.get({'id': keys['id']})['list'][0])

    @property
    def id(self) -> str:
        return self._basic_prop(self._id)

    @property
    def type(self) -> str:
        return self._basic_prop(self._type)

    @property
    def description(self) -> Dict:
        return self._basic_prop(self._description)

    @property
    def archived(self) -> datetime:
        return self._ts_to_dt(self._archived) if self._archived != '0' else None

    @property
    def images(self) -> List:
        return self._basic_prop(self._images)

    @property
    def files(self) -> List:
        return self._basic_prop(self._files)

    @property
    def flags(self) -> List[str]:
        return self._basic_prop(self._flags)

    @property
    def created(self) -> datetime:
        return self._ts_to_dt(self._created) if self._created else None

    @property
    def changed(self) -> datetime:
        return self._ts_to_dt(self._changed)

    @property
    def uid(self) -> int:
        return int(self._uid) if self._uid else None

    @property
    def data(self) -> str:
        return self._basic_prop(self._data)


class Planting(Asset):

    @property
    def crop(self) ->  List[Crop]:
        return self._get_terms(self._crop, Crop) if self._crop else None


class Animal(Asset):

    @property
    def animal_type(self) -> str:
        return self._basic_prop(self._animal_type)

    @property
    def nicknames(self) -> List[str]:
        return self._basic_prop(self._animal_nicknames)

    @property
    def castrated(self) -> bool:
        return self._basic_prop(self._animal_castrated)

    @property
    def sex(self) -> str:
        return self._basic_prop(self._animal_sex)

    @property
    def tag(self):
        return self._basic_prop(self._tag)

    @property
    def parent(self) -> List:
        return self._get_assets(self._parent, Animal) if self._parent else None

    @property
    def birth_date(self) -> datetime:
        return self._ts_to_dt(self._date)


class Equipment(Asset):

    @property
    def manufacturer(self) -> str:
        return self._basic_prop(self._manufacturer)

    @property
    def model(self) -> str:
        return self._basic_prop(self._model)

    @property
    def serial_number(self) -> str:
        return self._basic_prop(self._serial_number)
