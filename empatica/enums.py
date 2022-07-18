from enum import Enum


class DataType(Enum):
    HR = "HR"
    EDA = "EDA"


class DataTypeNotImplementedError(NotImplementedError):
    def __init__(self):
        super(DataTypeNotImplementedError, self).__init__("This datatype is not implemented yet")


class ActivityType(Enum):
    Camp = "camp"
    VR = "vr"
    All = "all"


class ActivityTypeNotImplementedError(NotImplementedError):
    def __init__(self):
        super(ActivityTypeNotImplementedError, self).__init__("This activity type is not implemented yet")
