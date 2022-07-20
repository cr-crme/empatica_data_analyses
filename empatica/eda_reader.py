import os
import pickle

from matplotlib import pyplot as plt
import numpy as np
from pyEDA.main import process_statistical

from .empatica_vrcamp_reader import EmpaticaVrCampReader
from .enums import ActivityType, TimeAxis


class EdaReader(EmpaticaVrCampReader):
    def __init__(self, data_path: str, timing_path: str, reprocess_eda: bool = True):
        super(EdaReader, self).__init__(data_path=data_path, timing_path=timing_path, n_cols=1)

        self.processed_data_path = f"{self.path[:self.path.index('.')]}_processed.pyeda"
        if reprocess_eda or not os.path.isfile(self.processed_data_path):
            self.pyeda_peaks = self._find_peaks()
            with open(self.processed_data_path, "wb+") as file:
                pickle.dump(self.pyeda_peaks, file)
        else:
            with open(self.processed_data_path, "rb") as file:
                self.pyeda_peaks = pickle.load(file)

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
        t = self._t_peak(activity_type)
        if reset_time_to_zero:
            t -= self.t(activity_type)[0]
        t /= time_axis
        ax.plot(t, self._peak(activity_type), "ro")

    def _t_peak(self, activity_type: ActivityType):
        return self.t(activity_type)[self.pyeda_peaks[activity_type][1]["indexlist"][0]]

    def _peak(self, activity_type: ActivityType):
        return np.array(self.pyeda_peaks[activity_type][1]["peaklist"]).T

    def extra_labels(self) -> tuple[str, ...]:
        return ("",)

    def _find_peaks(self):
        """Use pyEDA to find the peaks for each of the activity"""
        meditation = process_statistical(
            self.data(ActivityType.MEDITATION),
            use_scipy=True,
            sample_rate=self.rate,
            new_sample_rate=self.rate,
            segment_width=self.data(ActivityType.MEDITATION).shape[0],
        )
        camp = process_statistical(
            self.data(ActivityType.Camp),
            use_scipy=True,
            sample_rate=self.rate,
            new_sample_rate=self.rate,
            segment_width=self.data(ActivityType.Camp).shape[0],
        )
        vr = process_statistical(
            self.data(ActivityType.VR),
            use_scipy=True,
            sample_rate=self.rate,
            new_sample_rate=self.rate,
            segment_width=self.data(ActivityType.VR).shape[0],
        )
        return {ActivityType.MEDITATION: meditation, ActivityType.Camp: camp, ActivityType.VR: vr}
