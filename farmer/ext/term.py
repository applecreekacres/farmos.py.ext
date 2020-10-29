
from typing import Dict, List

from farmer.ext.farmobj import FarmObj
from farmer.ext.term import Crop, Term
from farmOS import farmOS


class Term(FarmObj):

    def __init__(self, farm: farmOS, keys: Dict):
        if 'resource' not in keys:
            super(Term, self).__init__(farm, keys)
        elif 'resource' in keys and keys['resource'] == 'taxonomy_term':
            super(Term, self).__init__(farm, farm.term.get(keys['id']))
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
        return self._basic_prop(self._description)

    @property
    def parent(self) -> List[Term]:
        return self._get_terms(self._parent, Term) if self._parent else None

    @property
    def vocabulary(self) -> Dict:
        return FarmObj(self, self._vocabulary) if self._vocabulary else None



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
        return CropFamily(self._farm, self._crop_family) if hasattr(self, '_crop_family') else None

    @property
    def images(self) -> List:
        return self._basic_prop(self._images)

    @property
    def maturity_days(self) -> int:
        return int(self._maturity_days) if self._maturity_days else None

    @property
    def parents_all(self) -> List[Crop]:
        return self._get_terms(self._parents_all, Crop) if self._parents_all else None

    @property
    def transplant_days(self) -> int:
        return int(self._transplant_days) if self._transplant_days else None


class Unit(FarmObj):
    pass


class Category(FarmObj):
    pass

