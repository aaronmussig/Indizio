from typing import Collection


def format_axis_label(label: str) -> str:
    """Format the axis label to be more human readable."""
    if len(label) > 10:
        return ''.join([f'{label[:3]}', '...', f'{label[-3:]}'])
    else:
        return label


def format_axis_labels(labels: Collection[str]) -> Collection[str]:
    """
    Format the axis labels to be more human readable.
    """
    return [format_axis_label(label) for label in labels]
