
from datetime import datetime
from typing import Any, Dict, List, Optional, Type

from farmOS import farmOS


class FarmObj(object):

    _farm: farmOS

    def __init__(self, farm: farmOS, keys: Dict = None):
        self._farm = farm
        self._keys = keys
        if keys:
            for key in keys:
                setattr(self, '_{}'.format(key), keys[key])

    def _get_terms(self, items: List[Dict], obj_class):
        li = []
        for item in items:
            rets = self._farm.term.get({"tid": item['id']})
            for ret in rets['list']:
                li.append(obj_class(self._farm, ret))
        return li

    def _get_logs(self, items: List[Dict], obj_class):
        li = []
        for item in items:
            rets = self._farm.log.get(item['id'])
            for ret in rets['list']:
                li.append(obj_class(self._farm, ret))
        return li

    def _get_areas(self, items: List[Dict], obj_class):
        li = []
        for item in items:
            rets = self._farm.area.get(item['id'])
            for ret in rets['list']:
                li.append(obj_class(self._farm, ret))
        return li

    def _get_assets(self, items: List[Dict], obj_class):
        li = []
        for item in items:
            rets = self._farm.asset.get(item['id'])
            if 'list' in rets:
                for ret in rets['list']:
                    li.append(obj_class(self._farm, ret))
            else:
                li.append(obj_class(self._farm, rets))
        return li

    @staticmethod
    def _basic_prop(prop: Any) -> Any:
        """Returns the argument if it is not None."""
        return prop if prop else None

    @staticmethod
    def _ts_to_dt(ts: int) -> Optional[datetime]:
        """Convert timestampt to datetime or return None."""
        return datetime.fromtimestamp(int(ts)) if ts else None

    def _get_key(self, key: str) -> Optional[str]:
        if key in self._keys:
            return self._keys[key]
        else:
            return None

    def _attr(self, key: str, ret_type: Type[Any]) -> Type[Any]:
        value = FarmObj._basic_prop(self._get_key(key))
        if value:
            return ret_type(value)
        else:
            return value

    @property
    def name(self) -> str:
        return FarmObj._basic_prop(self._keys['name'])
