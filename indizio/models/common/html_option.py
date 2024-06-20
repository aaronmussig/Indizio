from enum import Enum


class HtmlOption(Enum):
    """
    This superclass wraps all HTML select options and provides helpful methods.

    Extend this class if additional known-value options are required AND will be
    displayed in the browser.
    """

    @classmethod
    def to_options(cls):
        return [{'label': x.value, 'value': x.value} for x in cls]
