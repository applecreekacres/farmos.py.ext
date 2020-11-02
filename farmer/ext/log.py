
from datetime import datetime
from typing import Dict, List, Optional

from farmer import Area
from farmer.ext.asset import Asset, Equipment
from farmer.ext.farmobj import FarmObj
from farmer.ext.others import Inventory, Quantity, Soil
from farmer.ext.term import Category, Unit
from farmOS import farmOS


class Log(FarmObj):

    def __init__(self, farm: farmOS, keys: Dict):
        if 'resource' not in keys:
            super(Log, self).__init__(farm, keys)
        elif 'resource' in keys and keys['resource'] == 'log':
            super(Log, self).__init__(
                farm, farm.log.get({'id': keys['id']})['list'][0])
        else:
            raise KeyError('Key resource does not have value log')

    @property
    def id(self) -> Optional[int]:
        key = self._keys['id']
        return int(key) if key else None

    @property
    def type(self) -> str:
        return FarmObj._basic_prop(self._keys['type'])

    @property
    def timestamp(self) -> Optional[datetime]:
        return FarmObj._ts_to_dt(self._keys['timestamp'])

    @property
    def done(self) -> bool:
        return bool(self._keys['done'])

    @property
    def notes(self) -> Optional[str]:
        return self._keys['notes']['value'] if self._keys['notes'] else None

    @property
    def asset(self) -> List[Asset]:
        key = self._keys['asset']
        return self._get_assets(key, Asset)

    @property
    def equipment(self) -> List[Equipment]:
        return self._get_assets(self._keys['equipment'], Equipment)

    @property
    def area(self) -> List[Area]:
        return self._get_areas(self._keys['area'], Area)

    @property
    def geofield(self) -> str:
        return FarmObj._basic_prop(self._keys['geofield'])

    @property
    def movement(self) -> List[Area]:
        return self._get_areas(self._keys['movement']['area'], Area)

    @property
    def membership(self):
        return FarmObj._basic_prop(self._keys['membership'])

    @property
    def quantity(self) -> List[Quantity]:
        if self._keys['quantity']:
            ret = []
            for quantity in self._keys['quantity']:
                ret.append(Quantity(measure=quantity['measure'],
                                    label=quantity['label'],
                                    value=quantity['value'],
                                    unit=quantity['unit'] if 'unit' in quantity else None))
            return ret
        return []

    @property
    def images(self) -> List:
        return FarmObj._basic_prop(self._keys['images'])

    @property
    def files(self) -> List:
        return FarmObj._basic_prop(self._keys['files'])

    @property
    def flags(self) -> str:
        return FarmObj._basic_prop(self._keys['flags'])

    @property
    def categories(self) -> List[Category]:
        key = self._keys['log_category']
        return [Category(self._farm, x) for x in key]

    @property
    def owner(self):
        return FarmObj._basic_prop(self._keys['log_owner'])

    @property
    def created(self) -> Optional[datetime]:
        return FarmObj._ts_to_dt(self._keys['created'])

    @property
    def changed(self) -> Optional[datetime]:
        return FarmObj._ts_to_dt(self._keys['changed'])

    @property
    def uid(self) -> Optional[int]:
        key = self._keys['uid']
        return int(key) if key else None

    @property
    def data(self) -> str:
        return FarmObj._basic_prop(self._keys['data'])

    @property
    def inventory(self) -> List[Inventory]:
        if self._keys['inventory']:
            ret = []
            for inventory in self._keys['inventory']:
                ret.append(Inventory(inventory['value'], inventory['asset']['id']))
            return ret
        return []


class LotLog(Log):

    @property
    def lot_number(self) -> str:
        return FarmObj._basic_prop(self._keys['lot_number'])


# TODO cleanup property returns
class MoneyLog(LotLog):

    @property
    def units(self) -> List[Unit]:
        return []

    @property
    def values(self) -> List:
        return []

    @property
    def total_price(self) -> float:
        return FarmObj._basic_prop(self._keys['total_price'])

    @property
    def unit_price(self) -> float:
        return FarmObj._basic_prop(self._keys['unit_price'])


class Input(LotLog):

    @property
    def material(self) -> str:
        return FarmObj._basic_prop(self._keys['material'])

    @property
    def purpose(self) -> str:
        return FarmObj._basic_prop(self._keys['input_purpose'])

    @property
    def method(self) -> str:
        return FarmObj._basic_prop(self._keys['input_method'])

    @property
    def source(self) -> str:
        return FarmObj._basic_prop(self._keys['input_source'])

    @property
    def date_purchase(self) -> Optional[datetime]:
        return FarmObj._ts_to_dt(self._keys['date_purchase'])


class Seeding(LotLog):

    @property
    def seed_source(self) -> str:
        return FarmObj._basic_prop(self._keys['seed_source'])


class Transplanting(Log):
    pass


class Harvest(LotLog):
    pass


class Observation(Log):
    pass


class Maintenance(Log):
    pass


class Purchase(MoneyLog):

    @property
    def seller(self) -> str:
        return FarmObj._basic_prop(self._keys['seller'])


class Birth(Log):
    pass


class Medical(Log):
    pass


class Sale(Log):

    @property
    def invoice_number(self) -> str:
        return FarmObj._basic_prop(self._keys['invoice_number'])

    @property
    def customer(self) -> str:
        return FarmObj._basic_prop(self._get_key('customer'))


class Activity(Log):
    pass


class SoilTest(Log):

    @property
    def soil_lab(self) -> str:
        return FarmObj._basic_prop(self._get_key('soil_lab'))

    # TODO Fix return
    @property
    def soil_names(self) -> List[Soil]:
        return []
