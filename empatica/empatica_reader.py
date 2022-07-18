import csv
import datetime
from matplotlib import pyplot as plt
import numpy as np


def _to_int(value):
    return int(value[: value.find(".")])


def _to_float(value):
    return float(value)


class EmpaticaReader:
    def __init__(self, path: str):
        self.path = path
        self.initial_t: int | None = None
        self.rate: int | None = None

        self.t_data, self.daytime_data, self.data = self._read_csv_data()
        self.data_vr, self.data_camp = self._split_data()

    def add_to_plot(self, in_hour: bool = False) -> None:
        """Add the current data to a predefined matplotlib.pyplot figure"""

        t = (self.t_data / 3600) if in_hour else self.t_data
        plt.plot(t, self.data)

    def _read_csv_data(self) -> tuple[np.ndarray, list[datetime], np.ndarray]:
        """Read data from a CSV file"""

        daytime_data = []
        t_data = []
        data = []
        with open(self.path) as file:
            read = csv.reader(file, delimiter="\n")
            for row in read:
                if not row:
                    continue
                if self.initial_t is None:
                    self.initial_t = datetime.datetime.fromtimestamp(_to_int(row[0]))
                elif self.rate is None:
                    self.rate = _to_int(row[0])
                else:
                    t_data.append(0 if not t_data else (t_data[-1] + 1 / self.rate))
                    daytime_data.append(datetime.timedelta(seconds=t_data[-1]) + self.initial_t)
                    data.append(_to_float(row[0]))
        return np.array(t_data), daytime_data, np.array(data)

    def _split_data(self) -> tuple[np.ndarray, np.ndarray]:
        data_vr = []
        data_camp = []
        return data_vr, data_camp
