
from dataclasses import dataclass
from farmer.ext.farmobj import FarmObj
from typing import Union, Dict
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


class User(FarmObj):
    pass


class Content(FarmObj):

    @property
    def api_version(self) -> Union[str, None]:
        return self._basic_prop(self._api_version)

    @property
    def system_of_measurement(self) -> Union[str, None]:
        return self._basic_prop(self._system_of_measurement)

    @property
    def metrics(self) -> Dict:
        return self._basic_prop(self._metrics)

    @property
    def mapbox_api_key(self) -> str:
        return self._basic_prop(self._mapbox_api_key)

    @property
    def languages(self) -> Dict:
        return self._basic_prop(self._languages)

    @property
    def google_maps_api_key(self) -> str:
        return self._basic_prop(self._google_maps_api_key)
