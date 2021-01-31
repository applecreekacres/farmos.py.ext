
import csv
from typing import Dict, List

# from datetime import datetime
# import requests


class WeatherCloud():

    def __init__(self, database=None) -> None:
        self._database = database
        self._data_file = None

    def __enter__(self) -> List[Dict]:
        data = []
        self._data_file = open(self._database, 'r', encoding='utf-16-le')
        data = csv.DictReader((line.replace('\0', '') for line in self._data_file), delimiter=';')
        return data

    def __exit__(self, exception_type, exception_value, exception_traceback):
        self._data_file.close()
