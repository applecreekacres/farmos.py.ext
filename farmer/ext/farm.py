"""Main farm access."""

from __future__ import annotations

import os
from datetime import datetime
from typing import Dict, List, Type

from farmOS import farmOS

HOST = None
USER = None
PASS = None


def farm():
    """Access to farm with provided credentials."""
    return Farm()


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
    _transplants = []
    _observations = []

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

    @property
    def transplants(self) -> List[Transplanting]:
        if not self._transplants:
            self._transplants = self._get_logs('farm_transplanting', Transplanting)
        return self._transplants

    @property
    def observations(self) -> List[Observation]:
        if not self._observations:
            self._observations = self._get_logs('farm_observation', Observation)
        return self._observations


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
            "timestamp": str(int(datetime.timestamp(date))),
            "log_category": [{
                "name": category
            }],
            "type": "farm_observation"
        }
        data.update(fields)
        if 'done' not in data:
            data['done'] = '1' if done else '0'
        ret = self.log.send(data)
        return ret

    def create_planting(self, crop: Crop, season: str, location: str) -> Planting:
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

    def create_seeding(self, planting: Planting, location: Area, crop: Crop, date: datetime, seeds: int, source=None, done=False) -> Seeding:
        name = "Seed {} {} {}".format(date.year, location.name, crop.name)
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
        ret = self._create_log(name, date, 'Plantings', fields, done=done)
        return Seeding(self, keys=ret)

    def create_transplant(self, planting: Planting, location: Area, date: datetime, fields=None, done=False):
        name = "Transplant {}".format(planting.name)
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
        if fields:
            data.update(fields)
        ret = self._create_log(name, date, 'Plantings', data, done=done)
        return Transplanting(self, ret)

    def create_harvest(self, planting: Planting, date: datetime, quantities: List[Quantity], done=False):
        name = "Harvest {} {}".format(date.year, planting._crop[0]['name'])
        data = {
            "type": "farm_harvest",
            "asset": [{
                "id": planting.id,
                "resource": "taxonomy_term"
            }]
        }

        if quantities:
            data["quantity"] = []
            for quantity in quantities:
                data["quantity"].append(quantity.to_dict())

        ret = self._create_log(name, date, 'Plantings', data, done=done)
        return Harvest(self, ret)

    def create_log(self, name: str, date: datetime, category: str, fields: Dict, done=False):
        return Log(self, self._create_log(name, date, category, fields, done))
