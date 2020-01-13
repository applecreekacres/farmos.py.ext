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

    def __init__(self, dictionary: Dict):
        for key in dictionary:
            setattr(self, key, dictionary[key])

    # def __repr__(self):
    #     return "<%s: %s>" % type(self).__name__, self.__dict__


class Season(Dict2Obj):
    pass


class CropFamily(Dict2Obj):

    def __init__(self, keys):
        for key in keys:
            if key == "vocabulary":
                setattr(self, key, TaxonomyVocabulary(keys[key]))
            elif key == "parents_all":
                for parent in keys[key]:
                    setattr(self, key, TaxonomyTerm(parent))
            else:
                setattr(self, key, keys[key])


class TaxonomyVocabulary(Dict2Obj):
    pass


class TaxonomyTerm(Dict2Obj):
    pass


class Area(Dict2Obj):
    pass


class Farm(farmOS):

    _areas = []
    _crop_families = []
    _seasons = []

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
