from matplotlib import pyplot as plt

from .enums import DataType, DataTypeNotLoadedError, DataTypeNotImplementedError, ActivityType, ActivityTypeNotImplementedError
from .acc_reader import AccReader
from .eda_reader import EdaReader
from .hr_reader import HrReader


class Subject:
    def __init__(self, id_number: str, dates: list[str], data_path_folder: str, load_acc: bool = False, load_eda: bool = True, load_hr: bool = True):
        self.id_number = id_number
        self.dates = dates
        self.data_path_folder = data_path_folder

        self.acc = []
        self.eda = []
        self.hr = []
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
                    )
                )

            if load_hr:
                self.hr.append(
                    HrReader(
                        data_path=self.data_path_folder + self.hr_filename(i),
                        timing_path=self.data_path_folder + "timings.xlsx",
                    )
                )

    def acc_filename(self, date_index):
        """Get the ACC file name associated to date_index"""
        return f"{self.id_number}_{self.dates[date_index]}_Empatica_{DataType.ACC.value}.csv"

    def eda_filename(self, date_index):
        """Get the EDA file name associated to date_index"""
        return f"{self.id_number}_{self.dates[date_index]}_Empatica_{DataType.EDA.value}.csv"

    def hr_filename(self, date_index):
        """Get the HR file name associated to date_index"""
        return f"{self.id_number}_{self.dates[date_index]}_Empatica_{DataType.HR.value}.csv"

    @property
    def n_dates(self):
        """Get the number of files there is for this subject"""
        return len(self.dates)

    def _parse_plot_labels(self, figure: plt.figure, to_plot: DataType, activity_type: ActivityType):
        """Determine the plot title function to the input data"""
        if to_plot == DataType.ACC:
            title = "Acceleration"
            ylabel = "Acceleration (m/s)"
        elif to_plot == DataType.EDA:
            title = "Skin conductance"
            ylabel = "Skin conductance (microS)"
        elif to_plot == DataType.HR:
            title = "Heart rate"
            ylabel = "Heart rate (bpm)"
        else:
            raise DataTypeNotImplementedError()

        if figure is None:
            title += f" of subject {self.id_number}"

        if activity_type == ActivityType.All:
            pass
        elif activity_type == ActivityType.Camp:
            title += " for 'Camp' activity"
        elif activity_type == ActivityType.VR:
            title += " for 'VR' activity"
        elif activity_type == ActivityType.MEDITATION:
            title += " during 'meditation'"
        else:
            raise ActivityTypeNotImplementedError()

        return title, ylabel

    def plot(
        self,
        to_plot: DataType,
        activity_type: ActivityType = ActivityType.All,
        date_indices: tuple[int, ...] = None,
        figure: plt.figure = None,
        **options,
    ) -> plt.figure:
        """Plot the requested data to a new figure"""
        title, ylabel = self._parse_plot_labels(figure, to_plot, activity_type)
        figure = plt.figure(title) if figure is None else plt.figure(figure)
        date_indices = range(self.n_dates) if date_indices is None else date_indices

        figure.canvas.manager.set_window_title(title)
        ax = figure.gca()
        ax.set_title(title)
        ax.set_ylabel(ylabel)
        ax.set_xlabel("Time (hour)")
        for i in date_indices:
            if to_plot == DataType.ACC:
                if not self.acc:
                    raise DataTypeNotLoadedError("Acceleration data were not loaded for this subject")
                self.acc[i].add_to_plot(ax=ax, activity_type=activity_type, **options)
            elif to_plot == DataType.EDA:
                if not self.eda:
                    raise DataTypeNotLoadedError("EDA data were not loaded for this subject")
                self.eda[i].add_to_plot(ax=ax, activity_type=activity_type, **options)
            elif to_plot == DataType.HR:
                if not self.hr:
                    raise DataTypeNotLoadedError("HR data were not loaded for this subject")
                self.hr[i].add_to_plot(ax=ax, activity_type=activity_type, **options)
            else:
                raise DataTypeNotImplementedError()

        return figure
