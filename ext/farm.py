"""Main farm access."""

from farmOS import farmOS
import os
from typing import Dict

HOST = None
USER = None
PASS = None


def farm():
    """Access to farm with provided credentials."""
    return Farm()


class Dict2Obj():

    def __init__(self, dictionary: Dict):
        for key in dictionary:
            setattr(self, key, dictionary[key])


class Farm(farmOS):

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

    def seasons(self):
        seasons = self.term.get("farm_season")
        for season in seasons['list']:
            yield Season(season)


class Season(Dict2Obj):

    def __init__(self, keys):
        super().__init__(keys)
