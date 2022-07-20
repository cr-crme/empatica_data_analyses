from enum import Enum


class DataType(Enum):
    ACC = "ACC"
    HR_BPM = "HR"
    EDA = "EDA"


class DataTypeNotImplementedError(NotImplementedError):
    def __init__(self):
        super(DataTypeNotImplementedError, self).__init__("This datatype is not implemented yet")


class DataTypeNotLoadedError(RuntimeError):
    pass


class ActivityType(Enum):
    Camp = "camp"
    VR = "vr"
    MEDITATION = "meditation"
    All = "all"


class ActivityTypeNotImplementedError(NotImplementedError):
    def __init__(self):
        super(ActivityTypeNotImplementedError, self).__init__("This activity type is not implemented yet")


class TimeAxis:
    SECOND = 1
    MINUTE = 60
    HOUR = 60*60
