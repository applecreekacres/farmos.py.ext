
from datetime import datetime
from typing import Dict, List

from farmOS import farmOS


class FarmObj(object):

    _farm = None

    def __init__(self, farm: farmOS, keys: Dict = None):
        self._farm = farm
        if keys:
            for key in keys:
                setattr(self, '_{}'.format(key), keys[key])

    def _get_terms(self, items: List[Dict], obj_class):
        li = []
        for item in items:
            rets = self._farm.term.get(item['tid'])
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

    def _basic_prop(self, prop):
        """Returns the argument if it is not None"""
        return prop if prop else None


    def _ts_to_dt(self, ts: int) -> datetime:
        """Convert timestampt to datetime or return None"""
        return datetime.fromtimestamp(int(ts)) if ts else None

    @property
    def name(self) -> str:
        return self._basic_prop(self._name)

    @property
    def url(self) -> str:
        return self._basic_prop(self._url)
