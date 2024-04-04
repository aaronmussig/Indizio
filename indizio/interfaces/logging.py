from enum import Enum


class LogLevel(str, Enum):
    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"

    def as_numeric(self):
        if self is LogLevel.DEBUG:
            return 10
        elif self is LogLevel.INFO:
            return 20
        elif self is LogLevel.WARNING:
            return 30
        elif self is LogLevel.ERROR:
            return 40
        elif self is LogLevel.CRITICAL:
            return 50
        else:
            return 20
