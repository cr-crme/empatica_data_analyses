from matplotlib import pyplot as plt
from empatica import ActivityType, DataType, Subject

data_path_folder = (
    "C:\\Users\\pariterre\\Nextcloud\\Documents\\Technopole\\Projets\\DanielleLevac\\Empatica data\\Data\\"
)
subjects = [
    Subject("01", ["2022-06-28", "2022-06-30", "2022-07-06", "2022-07-08"], data_path_folder),
    Subject("02", ["2022-07-04", "2022-07-05", "2022-07-06"], data_path_folder),
    Subject("03", ["2022-06-27", "2022-06-29", "2022-07-05", "2022-07-07"], data_path_folder),
    Subject("04", ["2022-06-29", "2022-07-07", "2022-07-08"], data_path_folder),
    Subject("05", ["2022-06-27", "2022-07-01"], data_path_folder),
    Subject("06", ["2022-06-30", "2022-07-04"], data_path_folder),
]
date_indices = (0,)


def main():
    fig_eda = None
    fig_hr = None
    for subject in subjects:
        fig_eda = subject.plot(
            to_plot=DataType.EDA, activity_type=ActivityType.Camp, figure=fig_eda, date_indices=date_indices, color="r"
        )
        fig_eda = subject.plot(
            to_plot=DataType.EDA, activity_type=ActivityType.VR, figure=fig_eda, date_indices=date_indices, color="b"
        )
        fig_hr = subject.plot(
            DataType.HR, activity_type=ActivityType.Camp, figure=fig_hr, date_indices=date_indices, color="r"
        )
        fig_hr = subject.plot(
            DataType.HR, activity_type=ActivityType.VR, figure=fig_hr, date_indices=date_indices, color="b"
        )
    fig_eda.legend()
    fig_hr.legend()
    plt.show()


if __name__ == "__main__":
    main()
