from .empatica_vrcamp_reader import EmpaticaVrCampReader
from .enums import ActivityType


class AccReader(EmpaticaVrCampReader):
    def __init__(self, data_path: str, timing_path: str):
        super(AccReader, self).__init__(data_path=data_path, timing_path=timing_path, n_cols=3)

    def extra_labels(self) -> tuple[str, ...]:
        return "x", "y", "z"

    def print_table(self, activity_type: ActivityType = ActivityType.All, **options) -> None:
        raise NotImplementedError("No table was implemented for AccReader data")
