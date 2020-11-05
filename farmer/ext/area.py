"""FarmOS Area objects."""

from __future__ import annotations

from typing import Dict, List, Union

from farmer.ext.asset import Asset
from farmer.ext.farmobj import FileFarmObj


class Area(FileFarmObj):
    """Area located within a Farm."""

    @property
    def assets(self) -> List[Asset]:
        """Assets assigned to area.

        Returns:
            Union[List[Asset], None]: [description]
        """
        return self.farm.assets(self._keys['assets'])

    @property
    def description(self) -> str:
        """Explanation string of the asset.

        This is not escaped for any formatting that is present.

        Returns:
            str: Unformatted string.
        """
        return Area._basic_prop(self._keys['description'])

    @property
    def flags(self) -> List[str]:
        """Flag items assigned.

        Returns:
            List[str]: Assigned flags by name.
        """
        return Area._basic_prop(self._keys['flags'])

    @property
    def geofield(self) -> List[Dict]:
        """Location of area in `Well-Known Text` format.

        Returns:
            List[Dict]: Described locations.
        """
        return Area._basic_prop(self._keys['geofield'])

    @property
    def parent(self) -> List[Area]:
        """Parent Area of this Area.

        Returns:
            List[Area]: Generally a single item but stored as a list.
        """
        return self.farm.areas(self._keys['parent'])

    @property
    def parents_all(self) -> List[Area]:
        """All parents.

        Returns:
            List[Area]: List of parents.
        """
        return self.farm.areas(self._keys['parents_all'], Area)

    @property
    def tid(self) -> Union[int, None]:
        """Taxonomy ID of item.

        Returns:
            Union[int, None]: Unique ID, none if there is no id but this should
            not occur.
        """
        return int(self._keys['tid']) if self._keys['tid'] else None

    @property
    def vocabulary(self) -> Dict:
        """Vocabulary item assigned.

        Returns:
            Dict: Vocabulary item with id and name.
        """
        return Area._basic_prop(self._keys['vocabulary'])
