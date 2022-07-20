from .empatica_vrcamp_reader import EmpaticaVrCampReader


class AccReader(EmpaticaVrCampReader):
    def __init__(self, data_path: str, timing_path: str):
        super(AccReader, self).__init__(data_path=data_path, timing_path=timing_path, n_cols=3)

    def extra_labels(self) -> tuple[str, ...]:
        return "x", "y", "z"
