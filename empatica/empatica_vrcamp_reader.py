from abc import ABC
import datetime

import openpyxl

from .empatica_reader import EmpaticaReader
from .enums import ActivityType, ActivityTypeNotImplementedError


class EmpaticaVrCampReader(EmpaticaReader, ABC):
    def __init__(self, data_path: str, n_cols: int, timing_path: str):
        super(EmpaticaVrCampReader, self).__init__(data_path, n_cols)
        self.timings = self._parse_timings(timing_path)
        self.vr_index, self.camp_index, self.meditation_index = self._parse_timings_indices()

    def t(self, activity_type: ActivityType = None):
        if activity_type is None:
            return super(EmpaticaVrCampReader, self).t()
        elif activity_type == ActivityType.Camp:
            return self.t_data[self.camp_index[0] : self.camp_index[1]]
        elif activity_type == ActivityType.VR:
            return self.t_data[self.vr_index[0] : self.vr_index[1]]
        elif activity_type == ActivityType.MEDITATION:
            return self.t_data[self.meditation_index[0] : self.meditation_index[1]]
        else:
            raise ActivityTypeNotImplementedError(activity_type)

    def daytime(self, activity_type: ActivityType = None):
        if activity_type is None:
            return super(EmpaticaVrCampReader, self).daytime()
        elif activity_type == ActivityType.Camp:
            return self.daytime_data[self.camp_index[0] : self.camp_index[1]]
        elif activity_type == ActivityType.VR:
            return self.daytime_data[self.vr_index[0] : self.vr_index[1]]
        elif activity_type == ActivityType.MEDITATION:
            return self.daytime_data[self.meditation_index[0] : self.meditation_index[1]]
        else:
            raise ActivityTypeNotImplementedError(activity_type)

    def data(self, activity_type: ActivityType = None):
        if activity_type is None:
            return super(EmpaticaVrCampReader, self).data()
        elif activity_type == ActivityType.Camp:
            return self.actual_data[self.camp_index[0] : self.camp_index[1], :]
        elif activity_type == ActivityType.VR:
            return self.actual_data[self.vr_index[0] : self.vr_index[1], :]
        elif activity_type == ActivityType.MEDITATION:
            return self.actual_data[self.meditation_index[0] : self.meditation_index[1], :]
        else:
            raise ActivityTypeNotImplementedError(activity_type)

    @property
    def longest_activity(self) -> ActivityType:
        """Find the longest activity"""
        current_length = -1
        current_activity = ActivityType.All
        for activity in (ActivityType.MEDITATION, ActivityType.Camp, ActivityType.MEDITATION):
            t = self.t(activity)
            if t[-1] - t[0] > current_length:
                current_length = t[-1] - t[0]
                current_activity = activity
        return current_activity

    def _parse_timings(self, timing_filepath: str) -> tuple[datetime, ...]:
        """Get the timing data for VR and Camp, based on the data in the timing file"""
        desired_columns = (
            "Time start VR",
            "Time end VR",
            "Time start camp",
            "Time end camp",
            "Time start meditation",
            "Time end meditation",
        )
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

    def _parse_timings_indices(self) -> tuple[tuple[int, int], tuple[int, int], tuple[int, int]]:
        """Split the data into VR and camp"""

        vr_starting_index = -1
        vr_ending_index = -1
        camp_starting_index = -1
        camp_ending_index = -1
        meditation_starting_index = -1
        meditation_ending_index = -1
        for i, daytime in enumerate(self.daytime_data):
            # Reminder, self.timings is organised as such: Time start VR, Time end VR, Time start camp,
            # Time end camp, Time start meditation, Time end meditation
            daytime_time = daytime.time()
            if vr_starting_index < 0 and self.timings[0] < daytime_time:
                vr_starting_index = i
            elif vr_ending_index < 0 and self.timings[1] < daytime_time:
                vr_ending_index = i
            elif camp_starting_index < 0 and self.timings[2] < daytime_time:
                camp_starting_index = i
            elif camp_ending_index < 0 and self.timings[3] < daytime_time:
                camp_ending_index = i
            elif meditation_starting_index < 0 and self.timings[4] < daytime_time:
                meditation_starting_index = i
            elif meditation_ending_index < 0 and self.timings[5] < daytime_time:
                meditation_ending_index = i

        if (
            vr_starting_index < 0
            or vr_ending_index < 0
            or camp_starting_index < 0
            or camp_ending_index < 0
            or meditation_starting_index < 0
            or meditation_ending_index < 0
        ):
            raise ValueError("The timings could not be read for the current subject and date")

        return (
            (vr_starting_index, vr_ending_index),
            (camp_starting_index, camp_ending_index),
            (meditation_starting_index, meditation_ending_index),
        )
