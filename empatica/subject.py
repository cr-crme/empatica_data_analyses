from matplotlib import pyplot as plt

from .enums import DataType, DataTypeNotImplementedError
from .eda_reader import EdaReader
from .hr_reader import HrReader


class Subject:
    def __init__(self, id_number: str, dates: list[str], data_path_folder):
        self.id_number = id_number
        self.dates = dates
        self.data_path_folder = data_path_folder

        self.eda = []
        self.hr = []
        for i in range(self.n_dates):
            self.eda.append(EdaReader(self.data_path_folder + self.eda_filename(i)))
            self.hr.append(HrReader(self.data_path_folder + self.hr_filename(i)))

    def eda_filename(self, date_index):
        return f"{self.id_number}_{self.dates[date_index]}_Empatica_{DataType.EDA.value}.csv"

    def hr_filename(self, date_index):
        return f"{self.id_number}_{self.dates[date_index]}_Empatica_{DataType.HR.value}.csv"

    @property
    def n_dates(self):
        return len(self.dates)

    def plot(self, to_plot: DataType):
        if to_plot == DataType.EDA:
            title = f"Skin conductance of subject {self.id_number}"
            ylabel = "Skin conductance (microS)"
        elif to_plot == DataType.HR:
            title = f"Heart rate of subject {self.id_number}"
            ylabel = "Heart rate (bpm)"
        else:
            raise DataTypeNotImplementedError()

        plt.figure(title)
        plt.title(title)
        plt.ylabel(ylabel)
        plt.xlabel("Time (hour)")
        for i in range(self.n_dates):
            if to_plot == DataType.EDA:
                self.eda[i].add_to_plot(in_hour=True)
            elif to_plot == DataType.HR:
                self.hr[i].add_to_plot(in_hour=True)
            else:
                raise DataTypeNotImplementedError()
        plt.legend(self.dates)
