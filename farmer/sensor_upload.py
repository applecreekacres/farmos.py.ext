"""Upload sensor data to server."""


# import easygui
import tkinter as tk
from datetime import datetime
from tkinter import filedialog

from farmer.ext.sensor import Sensor
from farmer.weathercloud import WeatherCloud

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
    data_uploaded = True
    start = datetime.now()
    while data_uploaded:
        # Reset flag after entering loop
        data_uploaded = False
        with WeatherCloud(DATA_FILE) as data:
            print("Uploading data from {}".format(DATA_FILE))
            for item in data:
                date = datetime.strptime(item["Date (America/Chicago)"], "%Y-%m-%d %H:%M:%S")
                if (not summary or not sensor.get(start=date, end=date)) and date >= first_good_sample_point:
                    record = {
                        "timestamp": date.timestamp()
                    }
                    for key in FIELD_MAPPING:
                        if item[FIELD_MAPPING[key]]:
                            record[key] = float(item[FIELD_MAPPING[key]].replace(',', ''))
                    print("Record for {} uploaded".format(date))
                    sensor.upload(record)
                    data_uploaded = True  # Set flag so that loop will come back and check file again
                # else:
                    # print("Record for {} will not be uploaded".format(record_date))
    total = datetime.now() - start
    print("Uploaded data in {}".format(total))


if __name__ == "__main__":
    main()
