"""Upload sensor data to server."""


# import easygui
import argparse
import tkinter as tk
from datetime import datetime
from tkinter import filedialog

from farmer.ext.sensor import Sensor
from farmer.weathercloud import WeatherCloud

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
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", required=False, action='store_true')
    parser.add_argument("-a", required=False, action='store_true')
    parser.add_argument("-p", required=False, action='store_true')
    args = parser.parse_args()
    dry_run = args.n
    all_points = args.a
    multi_passes = args.p
    sensor = Sensor()
    summary = sensor.summary()
    data_uploaded = True
    passes = 0
    start = datetime.now()
    while data_uploaded:
        # Reset flag after entering loop if doing multiple passes
        data_uploaded = False if not multi_passes else True
        passes += 1
        with WeatherCloud(DATA_FILE) as data:
            print("Uploading data from {}".format(DATA_FILE))
            for item in data:
                date = datetime.strptime(item["Date (America/Chicago)"], "%Y-%m-%d %H:%M:%S")
                if all_points:
                    upload = (not summary or not sensor.get(start=date, end=date)) and date >= first_good_sample_point
                else:
                    upload = (not summary or int(summary['temperature']['last']) < date.timestamp())
                if upload:
                    record = {
                        "timestamp": date.timestamp()
                    }
                    for key in FIELD_MAPPING:
                        if item[FIELD_MAPPING[key]]:
                            record[key] = float(item[FIELD_MAPPING[key]].replace(',', ''))
                    print("Record for {} uploaded".format(date))
                    if not dry_run:
                        sensor.upload(record)
                    data_uploaded = True  # Set flag so that loop will come back and check file again
                else:
                    print("Record for {} will not be uploaded".format(date))
        data_uploaded = data_uploaded if multi_passes else False
    total = datetime.now() - start
    print("Uploaded data in {}".format(total))
    print("Made {} passes".format(passes))


if __name__ == "__main__":
    main()
