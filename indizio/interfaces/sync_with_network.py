from indizio.interfaces.html_option import HtmlOption


class SyncWithNetwork(HtmlOption):
    """
    This class is used to represent the options for showing edge weight in the graph.
    """
    DISABLED = 'Disabled'
    VISIBLE = 'Visible nodes'
    SELECTED = 'Selected nodes'
