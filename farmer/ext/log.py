
from datetime import datetime
from farmer.ext.others import Quantity
from typing import Dict, List

from farmer.ext.area import Area
from farmer.ext.asset import Asset, Equipment
from farmer.ext.farmobj import FarmObj
from farmer.ext.term import Category
from farmOS import farmOS


class Log(FarmObj):

    def __init__(self, farm: farmOS, keys: Dict):
        if 'resource' not in keys:
            super(Log, self).__init__(farm, keys)
        elif 'resource' in keys and keys['resource'] == 'log':
            super(Log, self).__init__(farm, farm.log.get({'id': keys['id']})['list'][0])
        else:
            raise KeyError('Key resource does not have value log')


    @property
    def id(self)-> int:
        return int(self._id) if self._id else None

    @property
    def type(self) -> str:
        return self._basic_prop(self._type)

    @property
    def timestamp(self) -> datetime:
        return self._ts_to_dt(self._timestamp)

    @property
    def done(self) -> bool:
        return bool(self._done) if self._done else None

    @property
    def notes(self) -> str:
        return self._notes['value'] if self._notes else None

    @property
    def asset(self) -> Asset:
        return self._get_assets(self._asset, Asset) if self._asset else None

    @property
    def equipment(self) -> List[Equipment]:
        return self._get_assets(self._equipment, Equipment) if self._equipment else None

    @property
    def area(self) -> List[Area]:
        return self._get_areas(self._area, Area) if self._area else None

    @property
    def geofield(self) -> str:
        return self._basic_prop(self._geofield)

    @property
    def movement(self) -> List[Area]:
        return self._get_areas(self._movement['area'], Area) if self._movement else None

    @property
    def membership(self):
        return self._basic_prop(self._membership)

    @property
    def quantity(self) -> List[Quantity]:
        if self._quantity:
            ret = []
            for quantity in self._quantity:
                ret.append(Quantity(measure=quantity['measure'],
                                    label=quantity['label'],
                                    value=quantity['value'],
                                    unit=quantity['unit'] if 'unit' in quantity else None))
            return ret
        return None

    @property
    def images(self) -> List:
        return self._basic_prop(self._images)

    @property
    def files(self) -> List:
        return self._basic_prop(self._files)

    @property
    def flags(self) -> str:
        return self._basic_prop(self._flags)

    @property
    def categories(self) -> List[Category]:
        return [Category(self._farm, x) for x in self._log_category] if self._log_category else None

    @property
    def owner(self):
        return self._basic_prop(self._log_owner)

    @property
    def created(self) -> datetime:
        return self._ts_to_dt(self._created)

    @property
    def changed(self) -> datetime:
        return self._ts_to_dt(self._changed)

    @property
    def uid(self) -> int:
        return int(self._uid) if self._uid else None

    @property
    def data(self) -> str:
        return self._basic_prop(self._data)



class Input(Log):

    @property
    def material(self) -> str:
        return self._basic_prop(self._material)

    @property
    def purpose(self) -> str:
        return self._basic_prop(self._input_purpose)

    @property
    def method(self) -> str:
        return self._basic_prop(self._input_method)

    @property
    def source(self) -> str:
        return self._basic_prop(self._input_source)

    @property
    def date_purchase(self) -> datetime:
        return self._ts_to_dt(self._date_purchase)

    @property
    def lot_number(self) -> str:
        return self._basic_prop(self._lot_number)


class Seeding(Log):
    pass


class Transplanting(Log):
    pass


class Harvest(Log):

    @property
    def lot_number(self) -> str:
        return self._basic_prop(self._lot_number)


class Expense(Log):
    pass



class Observation(Log):
    pass
