
# pylint: disable=invalid-name

from datetime import datetime, timedelta

import matplotlib.pyplot as plt

from farmer.ext.sensor import Sensor

def main():
    sensor = Sensor()
    record = sensor.get('temperature', datetime(2021, 1, 1, 0, 0, 0), datetime.now(), 0)

    x, y = build_data(record)
    hour_pts, hour_min, hour_max, hour_avg = calculate_metrics(x, y)
    plot_data(hour_pts, hour_min, hour_max, hour_avg)


def plot_data(hour_pts, hour_min, hour_max, hour_avg):
    plt.plot(hour_pts, hour_min, 'b-', hour_pts, hour_max, 'r-', hour_pts, hour_avg, 'g-')
    plt.ylabel('temperature')
    # plt.axis([x[0], x[-1], -10, 60])
    plt.show()


def calculate_metrics(x, y):
    hour_min = []
    hour_avg = []
    hour_max = []
    hour_pts = []
    for year in range(x[0].year, x[-1].year + 1):
        for month in range(x[0].month, x[-1].month + 1):
            for day in range(1, x[-1].day + 1):
                for hour in range(0, 24):
                    point_indices = [x.index(time) for time in x if datetime(
                        year, month, day, hour, time.minute) == time]
                    values = [y[index] for index in point_indices]
                    if values:
                        hour_min.append(min(values))
                        hour_max.append(max(values))
                        hour_avg.append(sum(values) / len(values))
                        hour_pts.append(datetime(year, month, day, hour) + timedelta(hours=1))
    return hour_pts, hour_min, hour_max, hour_avg


def build_data(record):
    x = []
    y = []
    for point in record:
        x.append(datetime.fromtimestamp(float(point['timestamp'])))
        y.append(float(point['name']))
    x.reverse()
    y.reverse()
    return x, y


if __name__ == "__main__":
    main()
