from indizio.models.common.html_option import HtmlOption


class BooleanAllAny(HtmlOption):
    """
    This class is used to represent the options for the boolean all/any.
    """
    ALL = 'All'
    ANY = 'Any'


class BooleanShowHide(HtmlOption):
    """
    This class is used to represent the options for the boolean show/hide.
    """
    SHOW = 'Show'
    HIDE = 'Hide'


class BooleanYesNo(HtmlOption):
    """
    This class is used to represent the options for the boolean yes/no.
    """
    YES = 'Yes'
    NO = 'No'
