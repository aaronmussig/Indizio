import logging
from datetime import datetime


class DashLoggerHandler(logging.StreamHandler):
    def __init__(self):
        logging.StreamHandler.__init__(self)
        self.queue = []

    def emit(self, record):
        # msg = self.format(record)
        ts = datetime.fromtimestamp(record.created).strftime('[%Y-%m-%d %H:%M:%S]')
        self.queue.append((ts, record.levelname, record.msg))


LOG = logging.getLogger()
LOG.setLevel(logging.DEBUG)
DASH_LOG_HANDLER = DashLoggerHandler()
# LOG.addHandler(DASH_LOG_HANDLER)
