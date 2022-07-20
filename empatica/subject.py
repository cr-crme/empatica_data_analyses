from matplotlib import pyplot as plt

from .enums import (
    DataType,
    DataTypeNotLoadedError,
    DataTypeNotImplementedError,
    ActivityType,
    ActivityTypeNotImplementedError,
)
from .acc_reader import AccReader
from .eda_reader import EdaReader
from .empatica_reader import EmpaticaReader
from .hr_bpm_reader import HrBpmReader
from .hr_ibi_reader import HrIbiReader


class Subject:
    def __init__(
        self,
        id_number: str,
        dates: list[str],
        data_path_folder: str,
        load_acc: bool = False,
        load_eda: bool = True,
        eda_segment_width: int = None,
        load_hr_bpm: bool = True,
        load_hr_ibi: bool = True,
        fast_load: bool = False,
    ):
        self.id_number = id_number
        self.dates = dates
        self.data_path_folder = data_path_folder

        self.acc = []
        self.eda = []
        self.hr_bpm = []
        self.hr_ibi = []
        for i in range(self.n_dates):
            if load_acc:
                self.acc.append(
                    AccReader(
                        data_path=self.data_path_folder + self.acc_filename(i),
                        timing_path=self.data_path_folder + "timings.xlsx",
                    )
                )

            if load_eda:
                self.eda.append(
                    EdaReader(
                        data_path=self.data_path_folder + self.eda_filename(i),
                        timing_path=self.data_path_folder + "timings.xlsx",
                        segment_width=eda_segment_width,
                        reprocess_eda=not fast_load,
                    )
                )

            if load_hr_bpm:
                self.hr_bpm.append(
                    HrBpmReader(
                        data_path=self.data_path_folder + self.hr_bpm_filename(i),
                        timing_path=self.data_path_folder + "timings.xlsx",
                    )
                )

            if load_hr_ibi:
                self.hr_ibi.append(
                    HrIbiReader(
                        data_path=self.data_path_folder + self.hr_ibi_filename(i),
                        timing_path=self.data_path_folder + "timings.xlsx",
                    )
                )

    def acc_filename(self, date_index):
        """Get the ACC file name associated to date_index"""
        return f"{self.id_number}_{self.dates[date_index]}_Empatica_{DataType.ACC.value}.csv"

    def eda_filename(self, date_index):
        """Get the EDA file name associated to date_index"""
        return f"{self.id_number}_{self.dates[date_index]}_Empatica_{DataType.EDA.value}.csv"

    def hr_bpm_filename(self, date_index):
        """Get the HR file name associated to date_index"""
        return f"{self.id_number}_{self.dates[date_index]}_Empatica_{DataType.HR_BPM.value}.csv"

    def hr_ibi_filename(self, date_index):
        """Get the HR file name associated to date_index"""
        return f"{self.id_number}_{self.dates[date_index]}_Empatica_{DataType.HR_IBI.value}.csv"

    def data(self, data_type: DataType) -> list[EmpaticaReader, ...]:
        if data_type == DataType.ACC:
            if not self.acc:
                raise DataTypeNotLoadedError("Acceleration data were not loaded for this subject")
            return self.acc
        elif data_type == DataType.EDA:
            if not self.eda:
                raise DataTypeNotLoadedError("EDA data were not loaded for this subject")
            return self.eda
        elif data_type == DataType.HR_BPM:
            if not self.hr_bpm:
                raise DataTypeNotLoadedError("HR (BPM) data were not loaded for this subject")
            return self.hr_bpm
        elif data_type == DataType.HR_IBI:
            if not self.hr_ibi:
                raise DataTypeNotLoadedError("HR (IBI) data were not loaded for this subject")
            return self.hr_ibi
        else:
            raise DataTypeNotImplementedError(data_type)

    @property
    def n_dates(self):
        """Get the number of files there is for this subject"""
        return len(self.dates)

    @staticmethod
    def _check_and_dispatch_declaration(elements, element, name, expected_len):
        if elements is None:
            elements = [element] * expected_len
        elif element is not None:
            raise ValueError(f"{name}s and {name} cannot be simultaneously defined")

        if len(elements) != expected_len:
            raise ValueError(f"{name}s and {name} should be of dimension 1 or {expected_len}")
        return elements

    def _parse_plot_labels(self, figure: plt.figure, data_type: DataType, activity_type: ActivityType):
        """Determine the plot title function to the input data"""
        if data_type == DataType.ACC:
            title = "Acceleration"
            y_label = "Acceleration (m/s)"
        elif data_type == DataType.EDA:
            title = "Skin conductance"
            y_label = "Skin conductance (microS)"
        elif data_type == DataType.HR_BPM:
            title = "Heart rate"
            y_label = "Heart rate (bpm)"
        elif data_type == DataType.HR_IBI:
            title = "Interbeat interval"
            y_label = "Interbeat interval (ms)"
        else:
            raise DataTypeNotImplementedError(data_type)

        if figure is None:
            title += f" of subject {self.id_number}"

        if figure is None:
            if activity_type == ActivityType.All:
                pass
            elif activity_type == ActivityType.Camp:
                title += " for 'Camp' activity"
            elif activity_type == ActivityType.VR:
                title += " for 'VR' activity"
            elif activity_type == ActivityType.MEDITATION:
                title += " during 'meditation'"
            else:
                raise ActivityTypeNotImplementedError(activity_type)

        return title, y_label

    def plot(
        self,
        data_type: DataType,
        activity_types: tuple[ActivityType, ...] = None,
        activity_type: ActivityType = None,
        date_indices: tuple[int, ...] = None,
        figure: plt.figure = None,
        plot_eda_peaks: bool = False,
        colors: tuple[str, ...] = None,
        color: str = None,
        **options,
    ) -> plt.figure:
        """Plot the requested data to a new figure"""

        activity_types = self._check_and_dispatch_declaration(
            activity_types, activity_type, "activity_type", len(activity_types) if activity_types is not None else 1
        )
        colors = self._check_and_dispatch_declaration(colors, color, "color", len(activity_types))

        date_indices = range(self.n_dates) if date_indices is None else date_indices
        title = ""
        y_label = ""
        for activity_type, color in zip(activity_types, colors):
            title, y_label = self._parse_plot_labels(figure, data_type, activity_type)
            figure = plt.figure(title) if figure is None else plt.figure(figure)
            figure.canvas.manager.set_window_title(title)

            ax = figure.gca()
            for date in date_indices:
                data = self.data(data_type)
                ax = data[date].add_to_plot(ax=ax, activity_type=activity_type, color=color, **options)
                if data_type == DataType.EDA and plot_eda_peaks:
                    self.eda[date].add_peaks_to_plot(ax=ax, activity_type=activity_type, **options)

        ax = figure.gca()
        ax.set_title(title)
        ax.set_ylabel(y_label)
        ax.set_xlabel("Time (hour)")
        return figure

    def print_table(
        self,
        data_type: DataType,
        date_indices: tuple[int, ...] = None,
    ) -> None:
        """Print relevant tables for the requested DataType and dates"""
        data = self.data(data_type)
        date_indices = range(self.n_dates) if date_indices is None else date_indices

        for date in date_indices:
            data[date].print_table()
