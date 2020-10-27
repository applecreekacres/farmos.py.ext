"""Main farm access."""

from datetime import date, datetime
import os
from typing import Dict, List, Type

from farmOS import farmOS
from farmOS.client import BaseAPI

HOST = None
USER = None
PASS = None


def farm():
    """Access to farm with provided credentials."""
    return Farm()


def _basic_prop(prop):
    return prop if prop else None


def _ts_to_dt(ts: str) -> datetime:
        return datetime.fromtimestamp(ts) if ts else None


class FarmObj(object):

    _farm = None

    def __init__(self, farm: farmOS, keys: Dict = None):
        self._ref_objs = {}
        self._farm = farm
        if keys:
            for key in keys:
                setattr(self, '_{}'.format(key), keys[key])

    def _get_terms(self, items: List[Dict], obj_class):
        li = []
        for item in items:
            rets = self._farm.term.get(item['tid'])
            for ret in rets['list']:
                li.append(obj_class(self._farm, ret))
        return li

    def _get_logs(self, items: List[Dict], obj_class):
        li = []
        for item in items:
            rets = self._farm.log.get(item['id'])
            for ret in rets['list']:
                li.append(obj_class(self._farm, ret))
        return li

    def _get_areas(self, items: List[Dict], obj_class):
        li = []
        for item in items:
            rets = self._farm.area.get(item['id'])
            for ret in rets['list']:
                li.append(obj_class(self._farm, ret))
        return li

    def _get_assets(self, items: List[Dict], obj_class):
        li = []
        for item in items:
            rets = self._farm.asset.get(item['id'])
            for ret in rets['list']:
                li.append(obj_class(self._farm, ret))
        return li

    @property
    def name(self) -> str:
        return _basic_prop(self._name)

    @property
    def url(self) -> str:
        return _basic_prop(self._url)


class Content(FarmObj):
    pass


class Term(FarmObj):

    def __init__(self, farm: farmOS, keys: Dict):
        if 'resource' not in keys:
            super(Term, self).__init__(farm, keys)
        elif 'resource' in keys and keys['resource'] == 'taxonomy_term':
            super(Term, self).__init__(farm, farm.term.get({'id': keys['id']})['list'][0])
        else:
            raise KeyError('Key resource does not have value taxonomy_term')

    @property
    def tid(self) -> int:
        return int(self._tid) if self._tid else None

    @property
    def weight(self) -> int:
        return int(self._weight) if self._weight else None

    @property
    def description(self) -> str:
        return _basic_prop(self._description)

    @property
    def parent(self):
        return self._get_terms(self._parent, Term) if self._parent else None

    @property
    def vocabulary(self):
        return _basic_prop(self._vocabulary)


class Asset(FarmObj):

    def __init__(self, farm, keys):
        if 'resource' not in keys:
            super(Asset, self).__init__(farm, keys)
        elif 'resource' in keys and keys['resource'] == 'farm_asset':
            super(Asset, self).__init__(farm, farm.asset.get({'id': keys['id']})['list'][0])

    @property
    def id(self) -> str:
        return _basic_prop(self._id)

    @property
    def type(self) -> str:
        return _basic_prop(self._type)

    @property
    def description(self) -> str:
        return _basic_prop(self._description)

    @property
    def archived(self) -> datetime:
        return _ts_to_dt(self._archived) if self._archived else None

    @property
    def images(self):
        return _basic_prop(self._images)

    @property
    def files(self):
        return _basic_prop(self._files)

    @property
    def flags(self) -> List[str]:
        return _basic_prop(self._flags)

    @property
    def created(self) -> datetime:
        return _ts_to_dt(self._created) if self._created else None

    @property
    def changed(self) -> datetime:
        return _ts_to_dt(self._changed)

    @property
    def uid(self) -> int:
        return int(self._uid) if self._uid else None

    @property
    def data(self) -> str:
        return _basic_prop(self._data)


class Area(FarmObj):

    @property
    def assets(self) -> List[Asset]:
        return self._get_assets(self._assets, Asset) if self._assets else None

    @property
    def description(self) ->  str:
        return _basic_prop(self._description)

    @property
    def files(self):
        return _basic_prop(self._files)

    @property
    def flags(self) -> List[str]:
        return _basic_prop(self._flags)

    @property
    def geofield(self) -> List[Dict]:
        return _basic_prop(self._geofield)

    @property
    def images(self):
        return _basic_prop(self._images)

    @property
    def parent(self) -> List:
        return self._get_areas(self._parent, Area) if self._parent else None

    @property
    def parents_all(self) ->  List:
        return self._get_areas(self._parents_all, Area) if self._parents_all else None

    @property
    def tid(self) -> int:
        return int(self._tid) if self._tid else None

    @property
    def vocabulary(self):
        return _basic_prop(self._vocabulary)


class User(FarmObj):
    pass


class Equipment(Asset):

    @property
    def manufacturer(self) -> str:
        return _basic_prop(self._manufacturer)

    @property
    def model(self) -> str:
        return _basic_prop(self._model)

    @property
    def serial_number(self) -> str:
        return _basic_prop(self._serial_number)


class Category(FarmObj):
    pass


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
    def type(self):
        return _basic_prop(self._type)

    @property
    def timestamp(self) -> datetime:
        return _ts_to_dt(self._timestamp)

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
    def equipment(self) -> Equipment:
        return self._get_assets(self._equipment, Equipment) if self._equipment else None

    @property
    def area(self) -> List[Area]:
        return self._get_areas(self._area, Area) if self._area else None

    @property
    def geofield(self) -> str:
        return _basic_prop(self._geofield)

    @property
    def movement(self):
        return _basic_prop(self._movement)

    @property
    def membership(self):
        return _basic_prop(self._membership)

    @property
    def quantity(self):
        return _basic_prop(self._quantity)

    @property
    def images(self):
        return _basic_prop(self._images)

    @property
    def files(self):
        return _basic_prop(self._files)

    @property
    def flags(self) -> str:
        return _basic_prop(self._flags)

    @property
    def categories(self) -> List[Category]:
        return [Category(self._farm, x) for x in self._log_category] if self._log_category else None

    @property
    def owner(self):
        return _basic_prop(self._log_owner)

    @property
    def created(self) -> datetime:
        return _ts_to_dt(self._created)

    @property
    def changed(self) -> datetime:
        return _ts_to_dt(self._changed)

    @property
    def uid(self) -> int:
        return int(self._uid) if self._uid else None

    @property
    def data(self) -> str:
        return _basic_prop(self._data)


class Season(Term):
    pass


class CropFamily(Term):
    pass


class Crop(Term):

    @property
    def companions(self):
        return self._get_terms(self._companions, Crop) if self._companions else None

    @property
    def crop_family(self) -> CropFamily:
        return CropFamily(self._farm, self._crop_family) if self._crop_family else None

    @property
    def images(self) -> List:
        return _basic_prop(self._images)

    @property
    def maturity_days(self) -> int:
        return int(self._maturity_days) if self._maturity_days else None

    @property
    def parents_all(self) -> List:
        return self._get_terms(self._parents_all, Crop) if self._parents_all else None

    @property
    def transplant_days(self) -> int:
        return int(self._transplant_days) if self._transplant_days else None


class Planting(Asset):

    @property
    def crop(self) ->  List[Crop]:
        return self._get_terms(self._crop, Crop) if self._crop else None


class Unit(FarmObj):
    pass


class Input(Log):

    @property
    def material(self):
        return _basic_prop(self._material)

    @property
    def purpose(self) -> str:
        return _basic_prop(self._input_purpose)

    @property
    def method(self) -> str:
        return _basic_prop(self._input_method)

    @property
    def source(self) -> str:
        return _basic_prop(self._input_source)

    @property
    def date_purchase(self) -> datetime:
        return _ts_to_dt(self._date_purchase)

    @property
    def lot_number(self) -> str:
        return _basic_prop(self._lot_number)


class Seeding(Log):
    pass


class Transplanting(Log):
    pass


class Harvest(Log):

    @property
    def lot_number(self) -> str:
        return _basic_prop(self._lot_number)


class Expense(Log):
    pass


class Animal(Asset):

    @property
    def animal_type(self) -> str:
        return _basic_prop(self._animal_type)

    @property
    def nicknames(self) -> List[str]:
        return _basic_prop(self._animal_nicknames)

    @property
    def castrated(self) -> bool:
        return _basic_prop(self._animal_castrated)

    @property
    def sex(self) -> str:
        return _basic_prop(self._animal_sex)

    @property
    def tag(self):
        return _basic_prop(self._tag)

    @property
    def parent(self) -> List:
        return self._get_assets(self._parent, Animal) if self._parent else None

    @property
    def birth_date(self) -> datetime:
        return _ts_to_dt(self._date)


class Farm(farmOS):

    _areas = []
    _crop_families = []
    _seasons = []
    _crops = []
    _content = None
    _equipment = []
    _planting = []
    _expenses = []
    _units = []
    _assets = []
    _harvests = []
    _seedings = []

    def __init__(self):
        if os.path.exists("farmos.cfg"):
            with open('farmos.cfg') as cfg:
                for line in cfg.readlines():
                    if line.startswith("HOST"):
                        HOST = line[line.index("=")+1:].strip()
                    if line.startswith("USER"):
                        USER = line[line.index("=")+1:].strip()
                    if line.startswith("PASS"):
                        PASS = line[line.index("=")+1:].strip()
            if not HOST:
                Exception("HOST key is not defined in farmos.cfg")
            if not USER:
                Exception("USER key is not defined in farmos.cfg")
            if not PASS:
                Exception("PASS key is not defined in farmos.cfg")
        super().__init__(HOST)
        self._token = self.authorize(USER, PASS)

    def reset(self):
        self._areas = []
        self._crop_families = []
        self._seasons = []
        self._crops = []
        self._content = None
        self._equipment = []
        self._planting = []
        self._assets = []
        self._harvests = []

    @property
    def content(self) -> Content:
        if not self._content:
            self._content = Content(self, keys=self.info())
        return self._content

    @property
    def seasons(self) -> List[Season]:
        if not self._seasons:
            response = self.term.get("farm_season")
            for season in response['list']:
                self._seasons.append(Season(self, season))
        return self._seasons

    @property
    def assets(self) ->  List[Asset]:
        if not self._assets:
            response = self.asset.get()
            for asset in response['list']:
                self._assets.append(Asset(self, keys=asset))
        return self._assets

    @property
    def areas(self) -> List[Area]:
        if not self._areas:
            response = self.area.get()
            for area in response['list']:
                self._areas.append(Area(self, keys=area))
        return self._areas

    @property
    def crop_families(self) -> List[CropFamily]:
        if not self._crop_families:
            response = self.term.get("farm_crop_families")
            for fam in response['list']:
                self._crop_families.append(CropFamily(self, keys=fam))
        return self._crop_families

    @property
    def crops(self) -> List[Crop]:
        if not self._crops:
            response = self.term.get("farm_crops")
            for crop in response['list']:
                c = Crop(self, crop)
                self._crops.append(c)
        return self._crops

    @property
    def equipment(self) ->  List[Equipment]:
        if not self._equipment:
            response = self.asset.get({
                'type': 'equipment'
            })
            for equip in response['list']:
                self._equipment.append(Equipment(self, equip))
        return self._equipment

    @property
    def plantings(self) -> List[Planting]:
        if not self._planting:
            response = self.asset.get({
                'type': 'planting'
            })
            for planting in response['list']:
                self._planting.append(Planting(self, planting))
        return self._planting

    @property
    def expenses(self) ->  List[Expense]:
        logs = self.log.get({
            'type': 'farm_activity'
        })
        for log in logs['list']:
            obj = Expense(self, log)
            if True:
                self._expenses.append(obj)
        return self._expenses

    @property
    def units(self) -> List[Unit]:
        units = self.term.get('farm_quantity_units')
        for unit in units['list']:
            self._units.append(Unit(self, unit))
        return self._units

    @property
    def harvests(self) -> List[Harvest]:
        if not self._harvests:
            self._harvests = self._get_logs('farm_harvest', Harvest)
        return self._harvests

    @property
    def seedings(self) -> List[Seeding]:
        if not self._seedings:
            self._seedings = self._get_logs('farm_seeding', Seeding)
        return self._seedings


    def _get_logs(self, typ: str, obj_class:  Type[Log]):
        li = []
        logs = self.log.get({'type': typ})
        for log in logs['list']:
            obj = obj_class(self, log)
            li.append(obj)
        return li

    def _create_log(self, name: str, date: datetime, category: str, fields: Dict, done=False):
        data = {
            "name": name,
            "timestamp": datetime.timestamp(date),
            "log_category": [{
                "name": category
            }],
            "type": "farm_observation"
        }
        data.update(fields)
        if 'done' not in data:
            data['done'] = 1 if done else 0
        ret = self.log.send(data)
        return ret

    def create_planting(self, crop: Crop, season: str, location: str):
        ret = self.asset.send({
            "name": "{} {} {}".format(season, location, crop.name),
            "type": "planting",
            "crop": [
                {
                    "id": crop.tid
                }
            ],
            "season": [{"name": season}]
        })
        plant = Planting(self, keys=ret)
        self._planting.append(plant)
        return plant

    def create_seeding(self, planting: Planting, location: Area, crop: Crop, date: datetime, seeds: int, source=None, done=False):
        name = "Seed {} {}".format(location.name, crop.name)
        fields = {
            "type": "farm_seeding",
            "asset": [
                {
                    "id": planting.id,
                    "resource": "taxonomy_term"
                }
            ],
            "seed_source": source,
            "movement": {
                "area": [
                    {
                        "id": location.tid,
                        "resource": "taxonomy_term"
                    }
                ]
            },
            "quantity": [
                {
                    "measure": "count",
                    "value": str(seeds),
                    "unit": {
                        'name': 'Seeds',
                        "resource": "taxonomy_term"
                    }
                }
            ]
        }
        ret = self._create_log(name, date, 'Plantings', fields)
        return Seeding(self, keys=ret)

    def create_transplant(self, planting: Planting, location: Area, date: datetime, done=False):
        name = "Transplant {} to {}".format(planting.crop[0]['name'], location.name)
        data = {
            "type": "farm_transplanting",
            "movement": {
                "area": [
                    {
                        "id": location.tid,
                        "resource": "taxonomy_term"
                    }
                ]
            },
            "asset": [
                {
                    "id": planting.id,
                    "resource": "taxonomy_term"
                }
            ]
        }
        ret = self._create_log(name, date, 'Plantings', data, done=done)
        return Transplanting(self, ret)

    def create_harvest(self, planting: Planting, date: datetime, done=False):
        name = "Harvest {}".format(planting.crop[0]['name'])
        data = {
            "type": "farm_harvest",
            "asset": [{
                "id": planting.id,
                "resource": "taxonomy_term"
            }]
        }
        ret = self._create_log(name, date, 'Plantings', data, done=done)
        return Harvest(self, ret)

    def create_log(self, name: str, date: datetime, category: str, fields: Dict, done=False):
        return Log(self, self._create_log(name, date, category, fields))
