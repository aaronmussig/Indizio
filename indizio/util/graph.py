from typing import Collection

from indizio.config import GRAPH_AXIS_MAX_LENGTH


def format_axis_label(label: str) -> str:
    """Format the axis label to be more human readable."""
    if len(label) > GRAPH_AXIS_MAX_LENGTH:
        return ''.join([f'{label[:5]}', '...', f'{label[-5:]}'])
    else:
        return label


def format_axis_labels(labels: Collection[str]) -> Collection[str]:
    """
    Format the axis labels to be more human readable.
    """
    return [format_axis_label(label) for label in labels]
