
from dataclasses import dataclass
from farmer.ext.farmobj import FarmObj
from typing import List, Type, Union, Dict
from enum import Enum


class Measure(Enum):
    COUNT = 'count'
    LENGTH = 'length'
    AREA = 'area'
    VOLUME = 'volume'
    TIME = 'time'
    TEMPERATURE = 'temperature'
    VALUE = 'value'
    RATE = 'rate'
    RATING = 'rating'
    RATIO = 'ratio'
    PROBABILITY = 'probability'
    WEIGHT = 'weight'


@dataclass
class Quantity():
    measure: Measure
    label: str
    unit: str
    value: str

    def to_dict(self):
        return {
            "measure": self.measure.value,
            "unit": {
                'name': self.unit,
                "resource": "taxonomy_term"
            },
            "value": self.value,
            "label": self.label
        }


@dataclass
class Inventory():
    value: int
    asset_id: int

    def to_dict(self):
        return {
            "asset": {"id": self.asset_id},
            "value": str(self.value)
        }


class User(FarmObj):
    pass


class Content(FarmObj):

    @property
    def api_version(self) -> Union[str, None]:
        return FarmObj._basic_prop(self._keys['api_version'])

    @property
    def system_of_measurement(self) -> Union[str, None]:
        return FarmObj._basic_prop(self._keys['system_of_measurement'])

    @property
    def metrics(self) -> Dict:
        return FarmObj._basic_prop(self._keys['metrics'])

    @property
    def mapbox_api_key(self) -> str:
        return FarmObj._basic_prop(self._keys['mapbox_api_key'])

    @property
    def languages(self) -> Dict:
        return FarmObj._basic_prop(self._keys['languages'])

    @property
    def google_maps_api_key(self) -> str:
        return FarmObj._basic_prop(self._keys['google_maps_api_key'])

    @property
    def resources(self) -> Dict:
        return FarmObj._basic_prop(self._keys['resources'])


class Soil(FarmObj):
    pass