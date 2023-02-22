from empatica import ActivityType, DataType, Subjects, PlotUtils, TableUtils


data_path_folder = (
    "C:\\Users\\pariterre\\Nextcloud\\Documents\\Technopole\\Projets\\DanielleLevac\\Empatica data\\Data\\\Empatica - raw data\\"
)

fast_load = True
eda_segment_width = None
show_eda_fig = False
plot_eda_peaks = False
show_eda_peak_fig = True
show_eda_table = True
show_hr_bpm_fig = False
show_hr_ibi_fig = False
should_savefig = True
figure_per_subject = True
date_indices = None  # (0,)


def main():
    subjects = Subjects(
        data_path_folder,
        fast_load=fast_load,
        eda_segment_width=eda_segment_width,
        load_eda=show_eda_fig or show_eda_table or show_eda_peak_fig,
        load_hr_bpm=show_hr_bpm_fig,
        load_hr_ibi=show_hr_ibi_fig,
    )

    subjects.add("01", ["2022-06-28", "2022-06-30", "2022-07-06", "2022-07-08"])
    subjects.add("02", ["2022-07-04", "2022-07-05", "2022-07-06"])
    subjects.add("03", ["2022-06-27", "2022-06-29", "2022-07-05"])  # "2022-07-07" <- No EDA peaks found
    subjects.add("04", ["2022-06-29", "2022-07-07", "2022-07-08"])
    subjects.add("05", ["2022-06-27", "2022-07-01"])
    subjects.add("06", ["2022-06-30", "2022-07-04"])
    date_labels = subjects.generate_date_axis_label()

    if show_eda_table:
        elements = TableUtils.print_document_header("results")
        print(r" \section*{Mean of all subjects}")
        subjects.print_table(
            data_type=DataType.EDA,
            activity_types=(ActivityType.BASELINE, ActivityType.Camp, ActivityType.VR),
            date_indices=date_indices,
        )
        print("")
        for subject in subjects:
            print(r" \newpage")
            print(r" \section*{Values of subject " + subject.id_number + "}")
            subject.print_table(
                data_type=DataType.EDA,
                activity_types=(ActivityType.BASELINE, ActivityType.Camp, ActivityType.VR),
                date_indices=date_indices,
            )
            print(r"")
        TableUtils.print_document_tail(elements)

    if show_eda_fig or show_hr_bpm_fig or show_hr_ibi_fig or show_eda_peak_fig:
        all_fig_eda = [None] * (len(subjects) if figure_per_subject else 1)
        all_fig_eda_peaks = [None] * (len(subjects) if figure_per_subject else 1)
        all_fig_hr_bpm = [None] * (len(subjects) if figure_per_subject else 1)
        all_fig_hr_ibi = [None] * (len(subjects) if figure_per_subject else 1)
        for i, subject in enumerate(subjects):
            i_plot = i if figure_per_subject else 0

            if show_eda_fig:
                all_fig_eda[i_plot] = subject.plot(
                    data_type=DataType.EDA,
                    activity_types=(ActivityType.BASELINE, ActivityType.Camp, ActivityType.VR),
                    figure=all_fig_eda[i_plot],
                    date_indices=date_indices,
                    colors=("g", "b", "r"),
                    plot_eda_peaks=plot_eda_peaks,
                )
            if show_eda_peak_fig:
                all_fig_eda_peaks[i_plot] = subject.plot_eda_figures(
                    activity_types=(ActivityType.BASELINE, ActivityType.Camp, ActivityType.VR),
                    figure=all_fig_eda_peaks[i_plot],
                    date_indices=date_indices,
                    colors=("g", "b", "r"),
                    x_axis=date_labels,
                    y_lim=(0, 10),
                )
            if show_hr_bpm_fig:
                all_fig_hr_bpm[i_plot] = subject.plot(
                    data_type=DataType.HR_BPM,
                    activity_types=(ActivityType.BASELINE, ActivityType.Camp, ActivityType.VR),
                    figure=all_fig_hr_bpm[i_plot],
                    date_indices=date_indices,
                    colors=("g", "b", "r"),
                )
            if show_hr_ibi_fig:
                all_fig_hr_ibi[i_plot] = subject.plot(
                    data_type=DataType.HR_IBI,
                    activity_types=(ActivityType.BASELINE, ActivityType.Camp, ActivityType.VR),
                    figure=all_fig_hr_ibi[i_plot],
                    date_indices=date_indices,
                    colors=("g", "b", "r"),
                )

        if should_savefig:
            if figure_per_subject:
                for i in range(len(subjects)):
                    PlotUtils.savefig(path_folder="results", fig=all_fig_eda[i], data_type=DataType.EDA, postfix=f"subject_{i}")
                    PlotUtils.savefig(path_folder="results", fig=all_fig_eda_peaks[i], data_type=DataType.EDA, postfix=f"peaks_subject_{i}")
                    PlotUtils.savefig(path_folder="results", fig=all_fig_hr_bpm[i], data_type=DataType.HR_BPM, postfix=f"subject_{i}")
                    PlotUtils.savefig(path_folder="results", fig=all_fig_hr_ibi[i], data_type=DataType.HR_IBI, postfix=f"subject_{i}")
            else:
                PlotUtils.savefig(path_folder="results", fig=all_fig_eda[0], data_type=DataType.EDA)
                PlotUtils.savefig(path_folder="results", fig=all_fig_eda_peaks[0], data_type=DataType.EDA, postfix="peaks")
                PlotUtils.savefig(path_folder="results", fig=all_fig_hr_bpm[0], data_type=DataType.HR_BPM)
                PlotUtils.savefig(path_folder="results", fig=all_fig_hr_ibi[0], data_type=DataType.HR_IBI)

        for fig_eda, fig_eda_peaks, fig_hr_bpm, fig_hr_ibi in zip(all_fig_eda, all_fig_eda_peaks, all_fig_hr_bpm, all_fig_hr_ibi):
            PlotUtils.add_legend(fig_eda)
            PlotUtils.add_legend(fig_eda_peaks)
            PlotUtils.add_legend(fig_hr_bpm)
            PlotUtils.add_legend(fig_hr_ibi)
        PlotUtils.show()


if __name__ == "__main__":
    main()
