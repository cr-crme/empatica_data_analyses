from empatica import ActivityType, DataType, Subject, PlotUtils


data_path_folder = (
    "C:\\Users\\pariterre\\Nextcloud\\Documents\\Technopole\\Projets\\DanielleLevac\\Empatica data\\Data\\"
)
subjects = [
    Subject("01", ["2022-06-28", "2022-06-30", "2022-07-06", "2022-07-08"], data_path_folder, fast_load=True),
    Subject("02", ["2022-07-04", "2022-07-05", "2022-07-06"], data_path_folder, fast_load=True),
    Subject("03", ["2022-06-27", "2022-06-29", "2022-07-05", "2022-07-07"], data_path_folder, fast_load=True),
    Subject("04", ["2022-06-29", "2022-07-07", "2022-07-08"], data_path_folder, fast_load=True),
    Subject("05", ["2022-06-27", "2022-07-01"], data_path_folder, fast_load=True),
    Subject("06", ["2022-06-30", "2022-07-04"], data_path_folder, fast_load=True),
]
subjects = [
    Subject("01", ["2022-06-28"], data_path_folder, fast_load=True),
]
date_indices = None  # (0,)
should_savefig = False


def main():
    fig_eda = None
    fig_hr_bpm = None
    fig_hr_ibi = None
    for subject in subjects:
        fig_eda = subject.plot(
            to_plot=DataType.EDA,
            activity_types=(ActivityType.MEDITATION, ActivityType.Camp, ActivityType.VR),
            figure=fig_eda,
            date_indices=date_indices,
            colors=("g", "b", "r"),
            plot_eda_peaks=False,
        )
        fig_hr_bpm = subject.plot(
            DataType.HR_BPM,
            activity_types=(ActivityType.MEDITATION, ActivityType.Camp, ActivityType.VR),
            figure=fig_hr_bpm,
            date_indices=date_indices,
            colors=("g", "b", "r"),
        )
        fig_hr_ibi = subject.plot(
            DataType.HR_IBI,
            activity_types=(ActivityType.MEDITATION, ActivityType.Camp, ActivityType.VR),
            figure=fig_hr_ibi,
            date_indices=date_indices,
            colors=("g", "b", "r"),
        )

    if should_savefig:
        PlotUtils.savefig(path_folder="results", fig=fig_eda, data_type=DataType.EDA, postfix='subject06')
        PlotUtils.savefig(path_folder="results", fig=fig_hr_bpm, data_type=DataType.HR_BPM, postfix='subject06')
        PlotUtils.savefig(path_folder="results", fig=fig_hr_ibi, data_type=DataType.HR_IBI, postfix='subject06')

    PlotUtils.add_legend(fig_eda)
    PlotUtils.add_legend(fig_hr_bpm)
    PlotUtils.add_legend(fig_hr_ibi)
    PlotUtils.show()


if __name__ == "__main__":
    main()
