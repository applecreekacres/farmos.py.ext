"""Main farm access."""

from __future__ import annotations

import os
from datetime import datetime
from typing import Dict, Iterable, Iterator, List, Type

from farmOS import farmOS

from farmer.ext.area import Area
from farmer.ext.asset import Asset, Equipment, Planting
from farmer.ext.log import (Activity, Birth, Harvest, Input, Log, Maintenance,
                            Medical, Observation, Purchase, Sale, Seeding,
                            SoilTest, Transplanting)
from farmer.ext.others import Content, Quantity
from farmer.ext.term import Crop, CropFamily, Season, Unit


class FarmTypeMissingError(Exception):
    pass


def farm():
    """Access to farm with provided credentials."""
    return Farm()


class Farm(farmOS):

    def __init__(self):
        self._host = None
        self._user = None
        self._pass = None

        if os.path.exists("farmos.cfg"):
            with open('farmos.cfg') as cfg:
                for line in cfg.readlines():
                    if line.startswith("HOST"):
                        self._host = line[line.index("=")+1:].strip()
                    if line.startswith("USER"):
                        self._user = line[line.index("=")+1:].strip()
                    if line.startswith("PASS"):
                        self._pass = line[line.index("=")+1:].strip()
            if not self._host:
                raise KeyError("HOST key is not defined in farmos.cfg")
            if not self._user:
                raise KeyError("USER key is not defined in farmos.cfg")
            if not self._pass:
                raise KeyError("PASS key is not defined in farmos.cfg")
            super().__init__(self._host)
            self._token = self.authorize(self._user, self._pass)
        else:
            raise Exception('farmos.cfg not found.')

    def _get_assets(self, obj_class: Type[Asset], filters={}) -> Iterator[Type[Asset]]:
        for asset in self.asset.get(filters)['list']:
            yield obj_class(self, asset)

    def _get_logs(self, obj_class: Type[Log], filters=None) -> Iterator[Type[Log]]:
        for log in self.log.get(filters)['list']:
            yield obj_class(self, log)

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

    @property
    def content(self) -> Content:
        return Content(self, keys=self.info())

    @property
    def seasons(self) -> Iterator[Season]:
        for season in self.term.get("farm_season")['list']:
            yield Season(self, season)

    def assets(self, filters={}) -> Iterable[Asset]:
        for asset in self.asset.get(filters)['list']:
            yield Asset(self, keys=asset)

    @property
    def areas(self) -> Iterable[Area]:
        for area in self.area.get()['list']:
            yield Area(self, keys=area)

    @property
    def crop_families(self) -> Iterable[CropFamily]:
        for fam in self.term.get("farm_crop_families")['list']:
            yield CropFamily(self, keys=fam)

    @property
    def crops(self) -> Iterable[Crop]:
        for crop in self.term.get("farm_crops")['list']:
            yield Crop(self, crop)

    def equipment(self, filters=dict()) -> Iterable[Equipment]:
        filters.update({'type': 'equipment'})
        return self._get_assets(Equipment, filters)

    def plantings(self, filters=dict()) -> Iterable[Planting]:
        filters.update({'type': 'planting'})
        return self._get_assets(Planting, filters)

    @property
    def units(self) -> Iterable[Unit]:
        for unit in self.term.get('farm_quantity_units')['list']:
            yield Unit(self, unit)

    def harvests(self, filters=dict()) -> Iterable[Harvest]:
        if 'farm_harvests' in self.content.resources['log']:
            filters.update({'type': 'farm_harvest'})
            return self._get_logs(Harvest, filters)
        else:
            raise FarmTypeMissingError("Harvest logs not supported.")

    def seedings(self, filters=dict()) -> Iterable[Seeding]:
        if 'farm_seedings' in self.content.resources['log']:
            filters.update({'type': 'farm_seeding'})
            return self._get_logs(Seeding, filters)
        else:
            raise FarmTypeMissingError("Seeding logs not supported.")

    def transplants(self, filters=dict()) -> Iterable[Transplanting]:
        if 'farm_transplanting' in self.content.resources['log']:
            filters.update({'type': 'farm_transplanting'})
            return self._get_logs(Transplanting, filters)
        else:
            raise FarmTypeMissingError("Transplanting logs not supported.")

    def observations(self, filters=dict()) -> Iterable[Observation]:
        if 'farm_observation' in self.content.resources['log']:
            filters.update({'type': 'farm_observation'})
            return self._get_logs(Observation, filters)
        else:
            raise FarmTypeMissingError("Observation logs not supported.")

    def maintenances(self, filters=dict()) -> Iterator[Maintenance]:
        if 'farm_maintenance' in self.content.resources['log']:
            filters.update({'type': 'farm_observation'})
            return self._get_logs(Maintenance, filters)
        else:
            raise FarmTypeMissingError("Maintenance logs not supported.")

    def purchases(self, filters=dict()) -> Iterator[Purchase]:
        if 'farm_purchase' in self.content.resources['log']:
            filters.update({'type': 'farm_purchase'})
            return self._get_logs(Purchase, filters)
        else:
            raise FarmTypeMissingError("Purchase logs not supported.")

    def sales(self, filters={}) -> Iterator[Sale]:
        if 'farm_sale' in self.content.resources['log']:
            filters.update({'type': 'farm_sale'})
            return self._get_logs(Sale, filters)
        else:
            raise FarmTypeMissingError("Sale logs not supported.")

    def births(self, filters={}) -> Iterator[Birth]:
        if 'farm_birth' in self.content.resources['log']:
            filters.update({'type': 'farm_birth'})
            return self._get_logs(Birth, filters)
        else:
            raise FarmTypeMissingError("Birth logs not supported.")

    def inputs(self, filters={}) -> Iterator[Input]:
        if 'farm_input' in self.content.resources['input']:
            filters.update({'type': 'farm_input'})
            return self._get_logs(Input, filters)
        else:
            raise FarmTypeMissingError("Input logs not supported.")

    def soil_tests(self, filters={}) -> Iterator[SoilTest]:
        if 'farm_soil_test' in self.content.resources['log']:
            filters.update({'type': 'farm_soil_test'})
            return self._get_logs(SoilTest, filters)
        else:
            raise FarmTypeMissingError("Soil test logs not supported.")

    def activities(self, filters={}) -> Iterator[Activity]:
        if 'farm_activity' in self.content.resources['log']:
            filters.update({'type': 'farm_activity'})
            return self._get_logs(Activity, filters)
        else:
            raise FarmTypeMissingError("Activity logs not supported.")

    def medicals(self, filters={}) -> Iterator[Medical]:
        if 'farm_medical' in self.content.resources['log']:
            filters.update({'type': 'farm_medical'})
            return self._get_logs(Medical, filters)
        else:
            raise FarmTypeMissingError("Medical logs are not supported.")

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
