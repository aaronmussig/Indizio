import logging
import os
from datetime import datetime

import rich

from indizio.interfaces.logging import LogLevel


def log(msg, level: LogLevel = LogLevel.INFO):
    # Check if this message should be displayed according to the level set
    min_level = os.environ.get('INDIZIO_LOG', 'info')
    min_level = LogLevel(min_level).as_numeric()
    if level.as_numeric() < min_level:
        return

    # Format the output message
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if level is LogLevel.DEBUG:
        color = 'blue'
    elif level is LogLevel.INFO:
        color = 'green'
    elif level is LogLevel.WARNING:
        color = 'yellow'
    elif level is LogLevel.ERROR:
        color = 'red'
    elif level is LogLevel.CRITICAL:
        color = 'red'
    else:
        color = 'green'

    rich.print(f'[bold][{ts}][/bold] [bold {color}]{level.value.upper()}[/bold {color}] - {msg}')


def log_debug(msg: str):
    log(msg, level=LogLevel.DEBUG)


def log_info(msg: str):
    log(msg, level=LogLevel.INFO)


def log_warn(msg: str):
    log(msg, level=LogLevel.WARNING)


def log_err(msg: str):
    log(msg, level=LogLevel.ERROR)


def hide_logs(name: str):
    logger = logging.getLogger(name)
    logger.setLevel(logging.WARNING)
