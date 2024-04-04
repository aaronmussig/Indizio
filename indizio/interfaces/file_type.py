from indizio.interfaces.html_option import HtmlOption


class UserFileType(HtmlOption):
    """
    These are the select options provided when a user uploads a file.
    """

    PA = 'Presence/Absence'
    DM = 'Distance Matrix'
    META = 'Metadata'
    TREE = 'Tree'
