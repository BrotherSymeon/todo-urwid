import logging
import logging.config
import socket

from datetime import datetime
from typing import Dict

import pytz


class LogRecordHostnameInjector(logging.Filter):
    _hostname = socket.gethostname()

    def filter(self, record: logging.LogRecord) -> bool:
        record.hostname = self._hostname
        return True


class LogRecordFormatter(logging.Formatter):
    """
    Override standard implementation to support both microseconds and TZ.

    See also:
        https://github.com/python/cpython/blob/v3.7.3/Lib/logging/__init__.py#L539-L563
        https://github.com/python/cpython/blob/v3.7.3/Lib/logging/__init__.py#L298
        https://github.com/python/cpython/blob/v3.7.3/Lib/_strptime.py#L457-L494

    """

    converter = datetime.fromtimestamp
    _tz = pytz.UTC

    def formatTime(self, record: logging.LogRecord, datefmt: str = None) -> str:
        ct = self.converter(record.created, self._tz)

        if datefmt:
            s = ct.strftime(datefmt)
        else:
            t = ct.strftime("%Y-%m-%d %H:%M:%S")
            s = "%s,%03d" % (t, record.msecs)

        return s


def setup_logging(config: Dict) -> None:
    logging.config.dictConfig(config)
