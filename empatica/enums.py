from enum import Enum


class DataType(Enum):
    HR = "HR"
    EDA = "EDA"


class DataTypeNotImplementedError(NotImplementedError):
    def __init__(self):
        super(DataTypeNotImplementedError, self).__init__("This datatype is not implemented yet")
