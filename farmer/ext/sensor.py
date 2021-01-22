

import json
import time
from datetime import datetime
from typing import Dict, List

import requests

FULL_URL = "{0}{1}{2}"
SENSOR_URL = "farm/sensor/listener/"


class Sensor():

    def __init__(self, farm: str, pub: str, prv: str = None) -> None:
        self._private_key = prv
        self._public_key = pub
        self._url = FULL_URL.format(farm, SENSOR_URL, pub)

    def upload(self, data: Dict, sleep=True):
        requests.post(self._url, params={"private_key": self._private_key}, json=data)
        if sleep:
            time.sleep(60)

    def get(self, name: str = None, start: datetime = None, end: datetime = None, limit: int = 0) -> List[Dict]:
        data = {}
        data['limit'] = limit
        if name:
            data['name'] = name
        if start:
            data['start'] = start.timestamp()
        if end:
            data['end'] = end.timestamp()
        if self._private_key:
            data['private_key'] = self._private_key
        req = requests.get(self._url, params=data)
        record = json.loads(req.text)
        return record

    def summary(self) -> Dict:
        return json.loads(requests.get("{}/summary".format(self._url), params={"private_key": self._private_key}).text)
