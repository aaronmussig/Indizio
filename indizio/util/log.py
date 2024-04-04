import logging
from typing import List

from indizio.interfaces.logging import LogLevel
import rich
from datetime import datetime
import os


def setup_logger(level):
    if level is LogLevel.DEBUG:
        level = logging.DEBUG
    elif level is LogLevel.INFO:
        level = logging.INFO
    elif level is LogLevel.WARNING:
        level = logging.WARNING
    elif level is LogLevel.ERROR:
        level = logging.ERROR
    elif level is LogLevel.CRITICAL:
        level = logging.CRITICAL
    else:
        level = logging.INFO
    logging.basicConfig(level=level, format='[%(asctime)s] - %(levelname)s - %(message)s')


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


def hide_logs(name: str):
    logger = logging.getLogger(name)
    logger.setLevel(logging.WARNING)
