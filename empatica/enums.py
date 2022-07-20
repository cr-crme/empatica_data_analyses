from enum import Enum


class DataType(Enum):
    ACC = "ACC"
    HR_BPM = "HR"
    HR_IBI = "IBI"
    EDA = "EDA"


class DataTypeNotImplementedError(NotImplementedError):
    def __init__(self, data_type: DataType):
        super(DataTypeNotImplementedError, self).__init__(f"This datatype ({data_type.value}) is not implemented yet")


class DataTypeNotLoadedError(RuntimeError):
    pass


class ActivityType(Enum):
    Camp = "camp"
    VR = "vr"
    MEDITATION = "meditation"
    All = "all"


class ActivityTypeNotImplementedError(NotImplementedError):
    def __init__(self, activity_type: ActivityType):
        super(ActivityTypeNotImplementedError, self).__init__(
            f"This activity type ({activity_type.value}) is not implemented yet"
        )


class TimeAxis:
    SECOND = 1
    MINUTE = 60
    HOUR = 60 * 60
