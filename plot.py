from empatica import ActivityType, DataType, Subject, PlotUtils


segment_width = None
fast_load = True
show_eda = True
show_hr_bpm = False
show_hr_ibi = False
should_savefig = False
date_indices = None  # (0,)

data_path_folder = (
    "C:\\Users\\pariterre\\Nextcloud\\Documents\\Technopole\\Projets\\DanielleLevac\\Empatica data\\Data\\"
)
subjects = [
    Subject(
        "01",
        ["2022-06-28", "2022-06-30", "2022-07-06", "2022-07-08"],
        data_path_folder,
        fast_load=fast_load,
        eda_segment_width=segment_width,
        load_eda=show_eda,
        load_hr_bpm=show_hr_bpm,
        load_hr_ibi=show_hr_ibi,
    ),
    Subject(
        "02",
        ["2022-07-04", "2022-07-05", "2022-07-06"],
        data_path_folder,
        fast_load=fast_load,
        eda_segment_width=segment_width,
        load_eda=show_eda,
        load_hr_bpm=show_hr_bpm,
        load_hr_ibi=show_hr_ibi,
    ),
    Subject(
        "03",
        ["2022-06-27", "2022-06-29", "2022-07-05", "2022-07-07"],
        data_path_folder,
        fast_load=fast_load,
        eda_segment_width=segment_width,
        load_eda=show_eda,
        load_hr_bpm=show_hr_bpm,
        load_hr_ibi=show_hr_ibi,
    ),
    Subject(
        "04",
        ["2022-06-29", "2022-07-07", "2022-07-08"],
        data_path_folder,
        fast_load=fast_load,
        eda_segment_width=segment_width,
        load_eda=show_eda,
        load_hr_bpm=show_hr_bpm,
        load_hr_ibi=show_hr_ibi,
    ),
    Subject(
        "05",
        ["2022-06-27", "2022-07-01"],
        data_path_folder,
        fast_load=fast_load,
        eda_segment_width=segment_width,
        load_eda=show_eda,
        load_hr_bpm=show_hr_bpm,
        load_hr_ibi=show_hr_ibi,
    ),
    Subject(
        "06",
        ["2022-06-30", "2022-07-04"],
        data_path_folder,
        fast_load=fast_load,
        eda_segment_width=segment_width,
        load_eda=show_eda,
        load_hr_bpm=show_hr_bpm,
        load_hr_ibi=show_hr_ibi,
    ),
]
# subjects = [
#     Subject(
#         "01",
#         ["2022-06-28"],
#         data_path_folder,
#         fast_load=fast_load,
#         eda_segment_width=segment_width,
#         load_eda=show_eda,
#         load_hr_bpm=show_hr_bpm,
#         load_hr_ibi=show_hr_ibi,
#     ),
# ]


def main():
    fig_eda = None
    fig_hr_bpm = None
    fig_hr_ibi = None
    for subject in subjects:
        if show_eda:
            fig_eda = subject.plot(
                to_plot=DataType.EDA,
                activity_types=(ActivityType.MEDITATION, ActivityType.Camp, ActivityType.VR),
                figure=fig_eda,
                date_indices=date_indices,
                colors=("g", "b", "r"),
                plot_eda_peaks=True,
            )
        if show_hr_bpm:
            fig_hr_bpm = subject.plot(
                DataType.HR_BPM,
                activity_types=(ActivityType.MEDITATION, ActivityType.Camp, ActivityType.VR),
                figure=fig_hr_bpm,
                date_indices=date_indices,
                colors=("g", "b", "r"),
            )
        if show_hr_ibi:
            fig_hr_ibi = subject.plot(
                DataType.HR_IBI,
                activity_types=(ActivityType.MEDITATION, ActivityType.Camp, ActivityType.VR),
                figure=fig_hr_ibi,
                date_indices=date_indices,
                colors=("g", "b", "r"),
            )

    if should_savefig:
        PlotUtils.savefig(path_folder="results", fig=fig_eda, data_type=DataType.EDA, postfix="subject01")
        PlotUtils.savefig(path_folder="results", fig=fig_hr_bpm, data_type=DataType.HR_BPM, postfix="subject01")
        PlotUtils.savefig(path_folder="results", fig=fig_hr_ibi, data_type=DataType.HR_IBI, postfix="subject01")

    PlotUtils.add_legend(fig_eda)
    PlotUtils.add_legend(fig_hr_bpm)
    PlotUtils.add_legend(fig_hr_ibi)
    PlotUtils.show()


if __name__ == "__main__":
    main()
