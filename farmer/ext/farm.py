"""Main farm access."""

from datetime import date, datetime
import os
from typing import Dict, List

from farmOS import farmOS
from farmOS.client import BaseAPI

HOST = None
USER = None
PASS = None


def farm():
    """Access to farm with provided credentials."""
    return Farm()


def _ref_key(obj, farm, keys: Dict, key: str, attr_class):

    if keys[key]['id']:
        setattr(obj, key, attr_class(farm, id_field=keys[key]['id']))
    del keys[key]


def _ref_key_list(obj, farm, key, keys_list, attr_class, exist=False):
    if keys_list[key]:
        if isinstance(keys_list[key], list):
            li = []
            for item in keys_list[key]:
                it = farm.get(int(item['id']))
                li.append(attr_class(it))
            setattr(obj, key, li)
        del keys_list[key]


class FarmObj(object):

    _farm = None

    def __init__(self, farm, keys: Dict = None):
        self._ref_objs = {}
        self._farm = farm
        if keys:
            self._attr_keys(keys)

    def __getattr__(self, name):
        if name in self._ref_objs:
            item = self._farm.term.get(int(self._ref_objs[name]['id']))
            setattr(self, name, FarmObj(self._farm, keys=item))

    def _attr_keys(self, keys):
        for key in keys:
            self._attr_key(key, keys, None, delete=False)

    def _attr_key(self, key, keys, exist=False, delete=True):
        if key in keys:
            if isinstance(keys[key], list):
                # li = []
                # for item in keys[key]:
                #     if isinstance(item, dict):
                #         if 'id' in item:
                #             refitem = self._farm.term.get(int(item['id']))
                #             obj = FarmObj(self._farm, keys=refitem)
                #         else:
                #             obj = FarmObj(self._farm, keys=item)
                #         li.append(obj)
                #     else:
                #         li.append(item)
                # setattr(self, key, li)
                setattr(self, key, keys[key])
            elif isinstance(keys[key], dict):
                self._ref_objs[key] = keys[key]
            else:
                setattr(self, key, keys[key])
            if delete:
                del keys[key]
        elif exist:
            setattr(self, key, None)

    def _get_obj(self, item):
        ref = None
        if item['resource'] == 'taxonomy_term':
            ref = self._farm.term.get(int(item['id']))
        # elif item['resource'] ==


class Term(FarmObj):
    pass


class Log(FarmObj):
    pass


class Asset(FarmObj):

    def __init__(self, farm, keys):
        if 'id' not in keys and 'resource' not in keys:
            super(Asset, self).__init__(farm, keys)
        elif 'resource' in keys and keys['resource'] == 'farm_asset':
            super(Asset, self).__init__(farm, farm.asset.get({'id': keys['id']})['list'][0])


class Season(Term):
    pass


class CropFamily(Term):
    pass


class Area(Asset):
    pass


class Crop(Term):
    pass


class Content(FarmObj):
    pass


class Equipment(Asset):
    pass


class Planting(Asset):
    pass


class User(FarmObj):
    pass


class Unit(FarmObj):
    pass


class Log(FarmObj):

    def __init__(self, farm, keys):
        if 'id' not in keys and 'resource' not in keys:
            super(Log, self).__init__(farm, keys)
        elif 'resource' in keys and keys['resource'] == 'log':
            super(Log, self).__init__(farm, farm.log.get({'id': keys['id']})['list'][0])
        else:
            raise KeyError('Key resource does not have value log')


class Seeding(Log):
    pass


class Transplanting(Log):
    pass


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

    def content(self):
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
    def assets(self):
        if not self._assets:
            response = self.asset.get()
            for asset in response['list']:
                self._assets.append(Asset(self, keys=asset))
        return self._assets

    @property
    def areas(self):
        if not self._areas:
            response = self.area.get()
            for area in response['list']:
                self._areas.append(Area(self, keys=area))
        return self._areas

    @property
    def crop_families(self):
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
    def equipment(self):
        if not self._equipment:
            response = self.asset.get({
                'type': 'equipment'
            })
            for equip in response['list']:
                self._equipment.append(Equipment(self, equip))
        return self._equipment

    @property
    def planting(self):
        if not self._planting:
            response = self.asset.get({
                'type': 'planting'
            })
            for planting in response['list']:
                self._planting.append(Planting(self, planting))
        return self._planting

    def create(self, type_name, fields):
        pass

    @property
    def expense_logs(self):
        logs = self.log.get({
            'type': 'farm_activity'
        })
        for log in logs['list']:
            obj = Log(self, log)
            if True:
                self._expenses.append(obj)
        return self._expenses

    @property
    def units(self):
        units = self.term.get('farm_quantity_units')
        for unit in units['list']:
            self._units.append(Unit(self, unit))
        return self._units

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

    def create_log(self, name: str, date: datetime, category: str, fields: Dict, done=False):
        return Log(self, self._create_log(name, date, category, fields))