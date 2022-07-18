from matplotlib import pyplot as plt
from empatica import ActivityType, DataType, Subject

data_path_folder = (
    "C:\\Users\\pariterre\\Nextcloud\\Documents\\Technopole\\Projets\\DanielleLevac\\Empatica data\\Data\\"
)
# subjects = [
#     Subject("01", ["2022-06-28", "2022-06-30", "2022-07-06", "2022-07-08"], data_path_folder, fast_load=True),
#     Subject("02", ["2022-07-04", "2022-07-05", "2022-07-06"], data_path_folder, fast_load=True),
#     Subject("03", ["2022-06-27", "2022-06-29", "2022-07-05", "2022-07-07"], data_path_folder, fast_load=True),
#     Subject("04", ["2022-06-29", "2022-07-07", "2022-07-08"], data_path_folder, fast_load=True),
#     Subject("05", ["2022-06-27", "2022-07-01"], data_path_folder, fast_load=True),
#     Subject("06", ["2022-06-30", "2022-07-04"], data_path_folder, fast_load=True),
# ]
subjects = [
    Subject("01", ["2022-06-28"], data_path_folder, fast_load=True),
]
date_indices = None  # (0,)


def savefig(fig: plt.figure, data_type: DataType, postfix: str):
    fig.legend()
    fig.set_size_inches(16, 9)
    fig.savefig(f"results/{data_type.value}_{postfix}.png", dpi=300)


def main():
    fig_eda = None
    fig_hr = None
    for subject in subjects:
        fig_eda = subject.plot(
            to_plot=DataType.EDA, activity_type=ActivityType.MEDITATION, figure=fig_eda, date_indices=date_indices, color="g", plot_eda_peaks=False
        )
        fig_eda = subject.plot(
            to_plot=DataType.EDA, activity_type=ActivityType.Camp, figure=fig_eda, date_indices=date_indices, color="b", plot_eda_peaks=False
        )
        fig_eda = subject.plot(
            to_plot=DataType.EDA, activity_type=ActivityType.VR, figure=fig_eda, date_indices=date_indices, color="r", plot_eda_peaks=False
        )
        fig_hr = subject.plot(
            DataType.HR, activity_type=ActivityType.MEDITATION, figure=fig_hr, date_indices=date_indices, color="g"
        )
        fig_hr = subject.plot(
            DataType.HR, activity_type=ActivityType.Camp, figure=fig_hr, date_indices=date_indices, color="b"
        )
        fig_hr = subject.plot(
            DataType.HR, activity_type=ActivityType.VR, figure=fig_hr, date_indices=date_indices, color="r"
        )

    # savefig(fig_eda, data_type=DataType.EDA, postfix='subject06')
    # savefig(fig_hr, data_type=DataType.HR, postfix='subject06')

    fig_eda.legend()
    fig_hr.legend()
    plt.show()


if __name__ == "__main__":
    main()
