from enum import Enum


class HtmlOption(Enum):
    """
    This superclass wraps all HTML select options and provides helpful methods.
    """

    @classmethod
    def to_options(cls):
        return [{'label': x.value, 'value': x.value} for x in cls]
