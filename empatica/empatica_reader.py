import csv
import datetime
from matplotlib import pyplot as plt
import numpy as np
import openpyxl

from .enums import ActivityType, ActivityTypeNotImplementedError


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


class EmpaticaReader:
    def __init__(self, data_path: str, timing_path: str, n_cols: int):
        self.path = data_path
        self.subject, self.date = _parse_name_and_date(self.path)
        self.initial_t: int | None = None
        self.rate: int | None = None
        self.n_cols = n_cols

        self.t_data, self.daytime_data, self.data = self._read_csv_data()
        self.timings = self._parse_timings(timing_path)
        self.vr_index, self.camp_index = self._parse_timings_indices()

    @property
    def t_data_camp(self):
        return self.t_data[self.camp_index[0] : self.camp_index[1]]

    @property
    def daytime_data_camp(self):
        return self.daytime_data[self.camp_index[0] : self.camp_index[1]]

    @property
    def data_camp(self):
        return self.data[self.camp_index[0] : self.camp_index[1], :]

    @property
    def t_data_vr(self):
        return self.t_data[self.vr_index[0] : self.vr_index[1]]

    @property
    def daytime_data_vr(self):
        return self.daytime_data[self.vr_index[0] : self.vr_index[1]]

    @property
    def data_vr(self):
        return self.data[self.vr_index[0] : self.vr_index[1], :]

    def add_to_plot(
        self,
        activity_type: ActivityType = ActivityType.All,
        in_hour: bool = False,
        reset_time_to_zero: bool = True,
        ax: plt.axes = None,
        **options,
    ) -> None:
        """Add the current data to a predefined matplotlib.pyplot figure"""
        if activity_type == ActivityType.All:
            t_data = self.t_data
            data = self.data
        elif activity_type == ActivityType.Camp:
            t_data = self.t_data_camp
            data = self.data_camp
        elif activity_type == ActivityType.VR:
            t_data = self.t_data_vr
            data = self.data_vr
        else:
            raise ActivityTypeNotImplementedError()

        t = (t_data / 3600) if in_hour else t_data
        if reset_time_to_zero:
            t -= t[0]

        if ax is None:
            ax = plt.gca()
        ax.plot(t, data, label=f"{self.subject} / {self.date} / {activity_type.value}", **options)

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
                    data.append(_to_float(row))
        return np.array(t_data), daytime_data, np.array(data)

    def _parse_timings(self, timing_filepath: str) -> tuple[datetime, ...]:
        """Get the timing data for VR and Camp, based on the data in the timing file"""
        desired_columns = ("Time start VR", "Time end VR", "Time start camp", "Time end camp")
        worksheet = openpyxl.load_workbook(timing_filepath).active

        is_header_parsed = False
        is_subject_found = False
        is_date_found = False
        are_data_found = False
        columns_mapping = []
        timings = [None] * len(desired_columns)
        for row in worksheet.iter_rows():
            for i_col, col in enumerate(row):
                if not is_header_parsed:
                    if col.value in desired_columns:
                        columns_mapping.append(i_col)
                    continue  # Go to next column

                if not is_subject_found:  # This assumes ID is before Date
                    if col.value != self.subject:
                        break  # We know we are not on the right row
                    is_subject_found = True
                    continue  # Go to next column

                if not is_date_found:  # This assumes Date is before the data
                    if str(col.value.date()) != self.date:
                        is_subject_found = False
                        break  # We know we are not on the right row
                    is_date_found = True
                    continue  # Go to next column

                # From now on, the data are sorted according to the desired_columns
                if i_col not in columns_mapping:
                    continue  # Go to next column
                are_data_found = True
                timings[columns_mapping.index(i_col)] = col.value
            is_header_parsed = True
            if are_data_found:
                break  # We already found the timings so no need to parse next rows

        return tuple(timings)

    def _parse_timings_indices(self) -> tuple[tuple[int, int], tuple[int, int]]:
        """Split the data into VR and camp"""

        vr_starting_index = -1
        vr_ending_index = -1
        camp_starting_index = -1
        camp_ending_index = -1
        for i, daytime in enumerate(self.daytime_data):
            # Reminder, self.timings is organised as such: Time start VR, Time end VR, Time start camp, Time end camp
            daytime_time = daytime.time()
            if vr_starting_index < 0 and self.timings[0] < daytime_time:
                vr_starting_index = i
            elif vr_ending_index < 0 and self.timings[1] < daytime_time:
                vr_ending_index = i
            elif camp_starting_index < 0 and self.timings[2] < daytime_time:
                camp_starting_index = i
            elif camp_ending_index < 0 and self.timings[3] < daytime_time:
                camp_ending_index = i

        if vr_starting_index < 0 or vr_ending_index < 0 or camp_starting_index < 0 or camp_ending_index < 0:
            raise ValueError("The timings could not be read for the current subject and date")

        return (vr_starting_index, vr_ending_index), (camp_starting_index, camp_ending_index)
