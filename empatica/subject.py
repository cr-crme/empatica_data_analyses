from .eda_reader import EdaReader


class Subject:
    def __init__(self, id: str, dates: list[str], data_path_folder):
        self.id = id
        self.dates = dates
        self.data_path_folder = data_path_folder

        self.eda = []
        for i in range(self.n_dates):
            self.eda.append(EdaReader(self.data_path_folder + self.eda_filename(i)))

    def eda_filename(self, date_index):
        return f"{self.id}_{self.dates[date_index]}_Empatica_EDA.csv"

    @property
    def n_dates(self):
        return len(self.dates)
