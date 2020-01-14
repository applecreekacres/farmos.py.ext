"""Main farm access."""

from farmOS import farmOS
import os
from typing import Dict, List

HOST = None
USER = None
PASS = None


def farm():
    """Access to farm with provided credentials."""
    return Farm()


class Dict2Obj(object):

    def __init__(self, keys: Dict):
        self._attr_key("vocabulary", keys, TaxonomyVocabulary)
        self._attr_key("parents_all", keys, TaxonomyTerm)
        for key in keys:
            self._attr_key(key, keys, None, delete=False)

    def _attr_key(self, key, keys, value, exist=False, delete=True):
        if key in keys:
            if isinstance(keys[key], list):
                li = []
                for item in keys[key]:
                    if value:
                        li.append(value(item))
                    else:
                        li.append(item)
                setattr(self, key, li)
            elif value:
                setattr(self, key, value(keys[key]))
            else:
                setattr(self, key, keys[key])
            if delete:
                del keys[key]
        elif exist:
            setattr(self, key, None)

    # def __repr__(self):
    #     return "<%s: %s>" % type(self).__name__, self.__dict__


class Season(Dict2Obj):
    pass


class CropFamily(Dict2Obj):
    pass


class TaxonomyVocabulary(Dict2Obj):
    pass


class TaxonomyTerm(Dict2Obj):
    pass


class Area(Dict2Obj):
    pass


class Crop(Dict2Obj):

    def __init__(self, keys):
        self._attr_key("crop_family", keys, CropFamily, exist=True)
        super().__init__(keys)


class Content(Dict2Obj):
    pass


class Farm(farmOS):

    _areas = []
    _crop_families = []
    _seasons = []
    _crops = []
    _content = None

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
        super().__init__(HOST, USER, PASS)
        self.authenticate()

    def reset(self):
        self._areas = []
        self._crop_families = []
        self._seasons = []
        self._crops = []
        self._content = None

    def content(self):
        if not self._content:
            self._content = Content(self.info())
        return self._content

    @property
    def seasons(self) -> List[Season]:
        if not self._seasons:
            response = self.term.get("farm_season")
            for season in response['list']:
                self._seasons.append(Season(season))
        return self._seasons

    @property
    def assets(self):
        pass

    @property
    def areas(self):
        if not self._areas:
            response = self.area.get()
            for area in response['list']:
                self._areas.append(Area(area))
        return self._areas

    @property
    def crop_families(self):
        if not self._crop_families:
            response = self.term.get("farm_crop_families")
            for fam in response['list']:
                self._crop_families.append(CropFamily(fam))
        return self._crop_families

    @property
    def crops(self) -> List[Crop]:
        if not self._crops:
            response = self.term.get("farm_crops")
            for crop in response['list']:
                c = Crop(crop)
                self._crops.append(c)
        return self._crops

    def create(self, type_name, fields):
        pass
