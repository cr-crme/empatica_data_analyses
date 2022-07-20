from abc import ABC, abstractmethod
import csv
import datetime
from matplotlib import pyplot as plt
import numpy as np

from .enums import ActivityType, TimeAxis


def _to_int(value) -> int:
    """Convert a str to an int"""
    return int(value[: value.find(".")])


def _to_float(values: list[str, ...]) -> list[float]:
    """Convert a str to a float"""
    return [float(value) for value in values]


def _parse_name_and_date(path: str) -> tuple[str, str]:
    subject = path.split("_")[0].split("\\")[-1]
    date = path.split("_")[1]
    return subject, date


class EmpaticaReader(ABC):
    def __init__(self, data_path: str, n_cols: int, rate: int = None):
        self.path = data_path
        self.subject, self.date = _parse_name_and_date(self.path)
        self.initial_t: int | None = None
        self.rate: int | None = rate
        self.n_cols = n_cols

        self.t_data, self.daytime_data, self.actual_data = self._read_csv_data()

    def t(self, activity_type: ActivityType = None):
        return self.t_data

    def daytime(self, activity_type: ActivityType = None):
        return self.daytime_data

    def data(self, activity_type: ActivityType = None):
        return self.actual_data

    @abstractmethod
    def extra_labels(self) -> tuple[str, ...]:
        """Returns the name of the data"""

    def add_to_plot(
        self,
        activity_type: ActivityType = ActivityType.All,
        time_axis: TimeAxis = TimeAxis.HOUR,
        reset_time_to_zero: bool = True,
        ax: plt.axes = None,
        norm: bool = False,
        **options,
    ) -> plt.axes:
        """Add the current data to a predefined matplotlib.pyplot figure"""
        t_data = self.t(activity_type)
        data = self.data(activity_type)
        data = np.linalg.norm(data, axis=1) if norm else data

        t = t_data / time_axis
        if reset_time_to_zero:
            t -= t[0]

        if ax is None:
            ax = plt.gca()

        label = f"{self.subject} / {self.date} / {activity_type.value}"
        if norm is None and self.extra_labels() is not None:
            label = [f"{label} / {extra_label}" for extra_label in self.extra_labels()]
        ax.plot(t, data, label=label, **options)
        return ax

    def _read_csv_data(self) -> tuple[np.ndarray, list[datetime], np.ndarray]:
        """Read data from a CSV file. The values must all collected at the same time at the same rate"""
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
                    data.append(_to_float(row[0].split(",")))
        return np.array(t_data), daytime_data, np.array(data)
