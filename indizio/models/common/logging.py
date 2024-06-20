from enum import Enum


class LogLevel(str, Enum):
    """
    This class is a helper method used to keep track of the logging level
    requested / messages used in the application.
    """
    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"

    def as_numeric(self):
        """
        This method is used to determine if the logging level is sufficient to
        display a message.
        """
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
