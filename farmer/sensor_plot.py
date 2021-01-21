
import requests
import json
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

#Attempt 2
PUB_KEY = "770eba8368bd4e29078cef0294b6ab2e"
PRV_KEY = "aa8ccf9b7a6ec56412851e041a72ea17"

# First Station created
# PUB_KEY = "8f47bee4b063bbf5ee712e246ea893fb"
# PRV_KEY = "de044e9af43acd486341e00f88e8b37b"

HOST = "https://applecreekacres.farmos.net/"
SENSOR_URL = "farm/sensor/listener/"
FULL_URL = "{0}{1}{2}".format(HOST, SENSOR_URL, PUB_KEY)
# FULL_URL = "{0}{1}{2}?private_key={3}".format(HOST, SENSOR_URL, PUB_KEY, PRV_KEY)


def main():
    data = {
        "private_key": PRV_KEY,
        "name": "temperature",
        "start": datetime(2021, 1, 1, 0, 0, 0).timestamp(),
        "end": datetime.now().timestamp(),
        "limit": 0
    }
    req = requests.get(FULL_URL, params=data)
    record = json.loads(req.text)
    x = []
    y = []
    for point in record:
        x.append(datetime.fromtimestamp(float(point['timestamp'])))
        y.append(float(point[data['name']]))
    x.reverse()
    y.reverse()
    hour_min = []
    hour_avg = []
    hour_max = []
    hour_pts = []
    for year in range(x[0].year, x[-1].year + 1):
        for month in range(x[0].month, x[-1].month + 1):
            for day in range(1, x[-1].day + 1):
                for hour in range(0, 24):
                    point_indices = [x.index(time) for time in x if datetime(year, month, day, hour, time.minute) == time]
                    values = [y[index] for index in point_indices]
                    if values:
                        hour_min.append(min(values))
                        hour_max.append(max(values))
                        hour_avg.append(sum(values) / len(values))
                        hour_pts.append(datetime(year, month, day, hour) + timedelta(hours=1))
                    pass

    plt.plot(hour_pts, hour_min, 'b-', hour_pts, hour_max, 'r-', hour_pts, hour_avg, 'g-')
    plt.ylabel(data['name'])
    # plt.axis([x[0], x[-1], -10, 60])
    plt.show()


if __name__ == "__main__":
    main()
