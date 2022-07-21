import numpy as np

from .enums import DataType, ActivityType
from .subject import Subject


class Subjects:
    def __init__(self,
        data_path_folder: str,
        load_acc: bool = False,
        load_eda: bool = True,
        eda_segment_width: int = None,
        load_hr_bpm: bool = True,
        load_hr_ibi: bool = True,
        fast_load: bool = False,
     ):
        self.subjects: list[Subject] = []
        self.data_path_folder = data_path_folder
        self.load_acc = load_acc
        self.load_eda = load_eda
        self.eda_segment_width = eda_segment_width
        self.load_hr_bpm = load_hr_bpm
        self.load_hr_ibi = load_hr_ibi
        self.fast_load = fast_load

        self._iter_index = 0

    def add(self,
        id_number: str,
        dates: list[str],
    ):
        self.subjects.append(Subject(id_number=id_number, dates=dates, data_path_folder=self.data_path_folder, load_acc=self.load_acc,
                load_eda=self.load_eda, eda_segment_width=self.eda_segment_width, load_hr_bpm=self.load_hr_bpm, load_hr_ibi=self.load_hr_ibi, fast_load=self.fast_load))

    def __getitem__(self, item) -> Subject:
        return self.subjects[item]

    def __iter__(self):
        return (s for s in self.subjects)

    def print_table(
            self,
            data_type: DataType,
            activity_types: tuple[ActivityType, ...] = None,
            activity_type: ActivityType = None,
            date_indices: tuple[int, ...] = None,
    ) -> None:
        """Print relevant tables for the requested DataType and dates"""

        # Prepare some values
        activity_types = Subject.check_and_dispatch_declaration(
            activity_types, activity_type, "activity_type", len(activity_types) if activity_types is not None else 1
        )
        data_to_print_mean = {}
        data_to_print_all_values = {}
        for activity_type in activity_types:
            data_to_print_all_values[activity_type] = []

        # Print the header of the table
        self.subjects[0].data(data_type)[0].print_table_header()

        for subject in self.subjects:
            data = subject.data(data_type)
            for date in range(subject.n_dates) if date_indices is None else date_indices:
                for activity_type in activity_types:
                    data_to_print_all_values[activity_type].append(data[date].get_table_value(activity_type))

        # Compute the mean of all values and print them
        for activity_type in activity_types:
            self.subjects[0].data(data_type)[0].print_table(activity_type, values=tuple(np.mean(data_to_print_all_values[activity_type], axis=0)))

        # Print the tail of the table
        self.subjects[0].data(data_type)[0].print_table_tail(f"Mean table for all the subjects")
