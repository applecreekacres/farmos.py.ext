

from __future__ import annotations

from typing import Dict, List

from farmer.ext.asset import Asset
from farmer.ext.farmobj import FarmObj, _basic_prop


class Area(FarmObj):

    @property
    def assets(self) -> List[Asset]:
        return self._get_assets(self._assets, Asset) if self._assets else None

    @property
    def description(self) ->  str:
        return _basic_prop(self._description)

    @property
    def files(self) -> List:
        return _basic_prop(self._files)

    @property
    def flags(self) -> List[str]:
        return _basic_prop(self._flags)

    @property
    def geofield(self) -> List[Dict]:
        return _basic_prop(self._geofield)

    @property
    def images(self) -> List:
        return _basic_prop(self._images)

    @property
    def parent(self) -> List[Area]:
        return self._get_areas(self._parent, Area) if self._parent else None

    @property
    def parents_all(self) ->  List:
        return self._get_areas(self._parents_all, Area) if self._parents_all else None

    @property
    def tid(self) -> int:
        return int(self._tid) if self._tid else None

    @property
    def vocabulary(self) -> Dict:
        return _basic_prop(self._vocabulary)
