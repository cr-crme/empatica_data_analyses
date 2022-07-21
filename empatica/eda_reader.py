import os
import pickle

from matplotlib import pyplot as plt
import numpy as np
from pyEDA.main import process_statistical

from .empatica_vrcamp_reader import EmpaticaVrCampReader
from .enums import ActivityType, TimeAxis


class EdaReader(EmpaticaVrCampReader):
    def __init__(self, data_path: str, timing_path: str, segment_width: int, reprocess_eda: bool = True):
        super(EdaReader, self).__init__(data_path=data_path, timing_path=timing_path, n_cols=1)

        self.baseline_value = self._compute_baseline()
        self._apply_baseline()

        self.segment_width = segment_width if segment_width is not None else np.inf
        self.processed_data_path = f"{self.path[:self.path.index('.')]}_processed.pyeda"
        if reprocess_eda or not os.path.isfile(self.processed_data_path):
            self.pyeda_peaks = self._find_peaks()
            with open(self.processed_data_path, "wb+") as file:
                pickle.dump(self.pyeda_peaks, file)
        else:
            with open(self.processed_data_path, "rb") as file:
                self.pyeda_peaks = pickle.load(file)

                # sanity check to make sure one is not loading data different from the requested segment_width
                if self.segment_width != np.inf and self.segment_width > self.t(self.longest_activity).size:
                    self.segment_width = np.inf
                data_segment_width = self._compute_segment_width_from_data(self.pyeda_peaks)
                if data_segment_width != self.segment_width:
                    raise RuntimeError(
                        f"The requested segment_width ({segment_width}) does not match the one from the "
                        f"preprocessed values ({data_segment_width}). Please use the same segment_width "
                        f"or set reprocess_eda to True (or fast_load to False)."
                    )

    def _compute_baseline(self) -> float:
        """Compute the baseline from the baseline trial"""
        return float(np.mean(self.data(ActivityType.BASELINE)))

    def _apply_baseline(self) -> None:
        """Apply the baseline values to all the data"""
        self.actual_data -= self.baseline_value

    def add_peaks_to_plot(
        self,
        activity_type: ActivityType,
        ax: plt.axes = None,
        reset_time_to_zero: bool = True,
        time_axis: TimeAxis = TimeAxis.HOUR,
        **_,
    ):
        if ax is None:
            ax = plt.gca()
        t = self.t_peak(activity_type)
        if reset_time_to_zero:
            t -= self.t(activity_type)[0]
        t /= time_axis
        ax.plot(t, self.peak(activity_type), "ro")

    def n_segments(self, activity_type: ActivityType) -> int:
        """Get the number of segments used to compute the peaks"""
        return len(self.pyeda_peaks[activity_type][0]["segment_indices"])

    def _compute_segment_width_from_data(self, data_peaks) -> int:
        """Find the length of the segmentation"""
        value = []
        for key in data_peaks:
            # Do not include last one, as it is of random size based on the length of the data acquisition
            value.extend([v[1] - v[0] for v in data_peaks[key][0]["segment_indices"][:-1]])
        if not all(v == value[0] for v in value):
            raise RuntimeError("A single value could not be found")

        # For all intend and purpose if the length of all the segment is the length of the segment,
        # then assume np.inf (or None) was used
        return int(value[0] / self.rate) if value else np.inf

    def t_per_segment(self, activity_type: ActivityType) -> list[np.ndarray, ...]:
        """Computes the time vector for each segment of the peaks"""
        full_t = self.t(activity_type)
        t_tp = []
        for i in range(self.n_segments(activity_type)):
            t_tp.append(
                full_t[
                    self.pyeda_peaks[activity_type][1]["indexlist"][i]
                    + self.pyeda_peaks[activity_type][0]["segment_indices"][i][0]
                ]
            )
        return t_tp

    def t_peak(self, activity_type: ActivityType) -> np.ndarray:
        """Returns the time vector for all the peak for all segments"""
        return np.concatenate(self.t_per_segment(activity_type))

    def peak_per_segment(self, activity_type: ActivityType) -> list[np.ndarray, ...]:
        """Get the peak values per segment"""
        return [np.array(data) for data in self.pyeda_peaks[activity_type][1]["peaklist"]]

    def peak(self, activity_type: ActivityType) -> np.ndarray:
        """Get the peak values for the full length of the activity"""
        return np.concatenate(self.peak_per_segment(activity_type))

    def extra_labels(self) -> tuple[str, ...]:
        return ("",)

    def _find_peaks(self):
        """Use pyEDA to find the peaks for each of the activity"""
        baseline = process_statistical(
            self.data(ActivityType.BASELINE),
            use_scipy=True,
            sample_rate=self.rate,
            new_sample_rate=self.rate,
            segment_width=self.segment_width,
        )
        camp = process_statistical(
            self.data(ActivityType.Camp),
            use_scipy=True,
            sample_rate=self.rate,
            new_sample_rate=self.rate,
            segment_width=self.segment_width,
        )
        vr = process_statistical(
            self.data(ActivityType.VR),
            use_scipy=True,
            sample_rate=self.rate,
            new_sample_rate=self.rate,
            segment_width=self.segment_width,
        )
        return {ActivityType.BASELINE: baseline, ActivityType.Camp: camp, ActivityType.VR: vr}

    def _table_columns(self) -> str:
        return "r|cccc"

    def _print_table_header(self) -> None:
        print(
            r"   Type of activity & \makecell{Mean number\\of peaks} & \makecell{Mean segment\\time (\SI{}{\second})} "
            r"& \makecell{Number of peaks\\per minute (\SI{}{1\per\minute})} "
            r"& \makecell{Mean max\\peak value (\SI{}{\micro\siemens})} \\"
        )

    def get_table_value(self, activity_type: ActivityType = ActivityType.All, **options) -> tuple:
        data = self.pyeda_peaks[activity_type]
        n_peaks = np.mean(data[0]["number_of_peaks"])
        total_time = np.mean([v[1] - v[0] for v in data[1]["segment_indices"]])
        peak_per_second = n_peaks / total_time * 60
        max_peak_value = np.mean(data[0]["max_of_peaks"])
        return n_peaks, total_time, peak_per_second, max_peak_value

    def print_table(self, activity_type: ActivityType = ActivityType.All, values: tuple = None, **options) -> None:
        if values is None:
            n_peaks, total_time, peak_per_second, max_peak_value = self.get_table_value(activity_type, **options)
        else:
            n_peaks, total_time, peak_per_second, max_peak_value = values
        print(
            rf"   {activity_type.value} & {n_peaks:0.1f} & {total_time:0.1f} & {peak_per_second:0.4f} & {max_peak_value:0.6f} \\"
        )
