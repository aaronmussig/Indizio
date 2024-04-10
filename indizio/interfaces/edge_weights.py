from indizio.interfaces.html_option import HtmlOption


class EdgeWeights(HtmlOption):
    """
    This class is used to represent the options for showing edge weight in the graph.
    """

    HIDDEN = 'Hidden'
    TEXT = 'Text'
    WEIGHT = 'Line weight'
    BOTH = 'Text & Line Weight'
