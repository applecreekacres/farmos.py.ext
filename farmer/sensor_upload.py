"""Upload sensor data to server."""

import csv
import json
import subprocess
import time
from datetime import datetime

# import easygui
import tkinter as tk
from tkinter import filedialog
import requests

from farmer.ext.sensor import Sensor
from farmer.weathercloud import WeatherCloud

# Attempt 2
PUB_KEY = "770eba8368bd4e29078cef0294b6ab2e"
PRV_KEY = "aa8ccf9b7a6ec56412851e041a72ea17"

# First Station created
# PUB_KEY = "8f47bee4b063bbf5ee712e246ea893fb"
# PRV_KEY = "de044e9af43acd486341e00f88e8b37b"

HOST = "https://applecreekacres.farmos.net/"

root = tk.Tk()
root.withdraw()
DATA_FILE = filedialog.askopenfilename()

FIELD_MAPPING = {
    "temperature": "Temp (°F)",
    "wind chill": "Chill (°F)",
    "dew point": "Dew (°F)",
    "humidity": "Hum (%)",
    "wind speed high": "Wspdhi (mph)",
    "wind speed avg": "Wspdavg (mph)",
    "wind direction avg": "Wdiravg (°)",
    "barometric pressure":  "Bar (hPa)",
    "rainfall": "Rain (in)",
    "rainfall rate": "Rainrate (in/h)",
    # "heat": "Heat (°F)"
}

first_good_sample_point = datetime(2020, 12, 26, 18, 00, 00)


def main():
    sensor = Sensor(HOST, PUB_KEY, PRV_KEY)
    summary = sensor.summary()
    with WeatherCloud(DATA_FILE) as data:
        for item in data:
            record_date = datetime.strptime(item["Date (America/Chicago)"], "%Y-%m-%d %H:%M:%S")
            if (not summary or not sensor.get('temperature', record_date, record_date)) and record_date >= first_good_sample_point:
                record = {
                    "timestamp": record_date.timestamp()
                }
                for key in FIELD_MAPPING:
                    if item[FIELD_MAPPING[key]]:
                        record[key] = float(item[FIELD_MAPPING[key]].replace(',', ''))
                sensor.upload(record, False)
                print("Record for {} uploaded".format(record_date))
                time.sleep(60)
            else:
                print("Record for {} will not be uploaded".format(record_date))


if __name__ == "__main__":
    main()
