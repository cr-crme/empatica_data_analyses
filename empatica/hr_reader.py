from .empatica_reader import EmpaticaReader


class HrReader(EmpaticaReader):
    def __init__(self, data_path: str, timing_path: str):
        super(HrReader, self).__init__(data_path=data_path, timing_path=timing_path, n_cols=1)

    def extra_labels(self) -> tuple[str, ...]:
        return "bpm",
