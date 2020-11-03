from __future__ import annotations

from datetime import datetime, timedelta
from typing import Dict, List, Optional

from farmOS import farmOS

from farmer.ext.farmobj import FarmObj


class Term(FarmObj):

    def __init__(self, farm: farmOS, keys: Dict):
        if 'resource' not in keys:
            super().__init__(farm, keys)
        elif 'resource' in keys and keys['resource'] == 'taxonomy_term':
            super().__init__(farm, farm.term.get(
                {"tid": int(keys['id'])})['list'][0])
        else:
            raise KeyError('Key resource does not have value taxonomy_term')

    @property
    def tid(self) -> Optional[int]:
        return int(self._keys['tid']) if self._keys['tid'] else None

    @property
    def weight(self) -> Optional[int]:
        return int(self._keys['weight']) if self._keys['weight'] else None

    @property
    def description(self) -> str:
        return FarmObj._basic_prop(self._keys['description'])

    @property
    def parent(self) -> List[Term]:
        return self._get_terms(self._keys['parent'], Term)

    @property
    def vocabulary(self) -> Optional[Dict]:
        return FarmObj._basic_prop(self._keys['vocabulary'])


class Season(Term):

    @property
    def start_date(self) -> Optional[datetime]:
        return FarmObj.timestamp_to_datetime(self._keys['date_range']['value'])

    @property
    def end_date(self) -> Optional[datetime]:
        return FarmObj.timestamp_to_datetime(self._keys['date_range']['value2'])

    @property
    def duration(self) -> Optional[timedelta]:
        if self.start_date and self.end_date:
            return self.end_date - self.start_date
        return None


class CropFamily(Term):
    pass


class Crop(Term):

    @property
    def companions(self) -> List[Crop]:
        return self._get_terms(self._keys['companions'], Crop)

    @property
    def crop_family(self) -> Optional[CropFamily]:
        key = self._keys['crop_family']
        return CropFamily(self._farm, key) if key else None

    @property
    def maturity_days(self) -> Optional[int]:
        key = self._keys['maturity_days']
        return int(self._keys['maturity_days']) if key else None

    @property
    def parents_all(self) -> List[Crop]:
        return self._get_terms(self._keys['parents_all'], Crop)

    @property
    def transplant_days(self) -> Optional[int]:
        key = self.key('transplant_days')
        return int(key) if key else None


class Unit(FarmObj):
    pass


class Category(FarmObj):
    pass
