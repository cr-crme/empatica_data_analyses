import empatica
from matplotlib import pyplot as plt

data_path_folder = "Data/Pilot/"
subjects = [
    empatica.Subject("01", ["2022-06-28", "2022-06-30", "2022-07-06", "2022-07-08"], data_path_folder),
    empatica.Subject("02", ["2022-07-04", "2022-07-05", "2022-07-06"], data_path_folder),
    empatica.Subject("03", ["2022-06-27", "2022-06-29", "2022-07-05", "2022-07-07"], data_path_folder),
    empatica.Subject("04", ["2022-06-29", "2022-07-07", "2022-07-08"], data_path_folder),
    empatica.Subject("05", ["2022-06-27", "2022-07-01"], data_path_folder),
    empatica.Subject("06", ["2022-06-30", "2022-07-04"], data_path_folder),
]


def main():
    for subject in subjects:
        plt.figure(f"Sujet : {subject.id}")
        plt.title(f"Data du sujet {subject.id}")
        plt.ylabel("Data (microS)")
        plt.xlabel("Time (hour)")
        for i in range(subject.n_dates):
            subject.eda[i].add_to_plot(hourly=True)
        plt.legend(subject.dates)
    plt.show()


if __name__ == "__main__":
    main()
