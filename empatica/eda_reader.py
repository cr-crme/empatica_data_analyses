import csv
import datetime
from matplotlib import pyplot as plt
import numpy as np


class EdaReader:
    def __init__(self, path: str):
        self.path = path
        self.initial_t: int | None = None
        self.rate: int | None = None

        self.t_data = []
        self.daytime_data = []
        self.data = []

        with open(self.path) as file:
            read = csv.reader(file, delimiter="\n")
            for row in read:
                if not row:
                    continue
                if self.initial_t is None:
                    self.initial_t = datetime.datetime.fromtimestamp(self._to_int(row[0]))
                elif self.rate is None:
                    self.rate = self._to_int(row[0])
                else:
                    self.t_data.append(0 if not self.t_data else (self.t_data[-1] + 1 / self.rate))
                    self.daytime_data.append(datetime.timedelta(seconds=self.t_data[-1]) + self.initial_t)
                    self.data.append(self._to_float(row[0]))

        self.t_data = np.array(self.t_data)
        self.data = np.array(self.data)

    def add_to_plot(self, hourly: bool = False):
        plt.plot((self.t_data / 3600) if hourly else self.t_data, self.data)

    @staticmethod
    def _to_int(value):
        return int(value[: value.find(".")])

    @staticmethod
    def _to_float(value):
        return float(value)
