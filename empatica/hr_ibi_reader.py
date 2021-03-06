from .empatica_vrcamp_reader import EmpaticaVrCampReader
from .enums import ActivityType


class HrIbiReader(EmpaticaVrCampReader):
    def __init__(self, data_path: str, timing_path: str):
        super(HrIbiReader, self).__init__(data_path=data_path, n_cols=2, timing_path=timing_path)

    def extra_labels(self) -> tuple[str, ...]:
        return ("hr ibi",)

    def _has_rate(self) -> bool:
        return False

    def _next_t(self, row, t_data) -> float:
        return self._to_float(row)[0]

    def _next_data(self, row) -> list[float]:
        return [super(HrIbiReader, self)._next_data(row)[1]]

    def _table_columns(self) -> str:
        raise NotImplementedError("No table was implemented for HrIbiReader data")

    def get_table_value(self, activity_type: ActivityType = ActivityType.All, **options) -> tuple:
        raise NotImplementedError("No table was implemented for HrIbiReader data")

    def _print_table_header(self) -> None:
        raise NotImplementedError("No table was implemented for HrIbiReader data")

    def print_table(self, activity_type: ActivityType = ActivityType.All, **options) -> None:
        raise NotImplementedError("No table was implemented for HrIbiReader data")
