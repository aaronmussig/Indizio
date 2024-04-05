from typing import Optional

import dash

from indizio.components.layout.message import LayoutMessage
from indizio.util.log import log_warn


def notify_user(message: str, exception: Optional[Exception] = None):
    """
    This message will automatically determine the ID for the notification Toast,
    it will then show the message. All other attributes will not be updated.
    """
    log_warn(message)
    out = dict()
    for k, d_prop in dash.callback_context.outputs_grouping.items():

        # Set the default state
        out[k] = dash.no_update

        # Obtain the information for the current output property
        cur_id = d_prop.get('id')
        cur_prop = d_prop.get('property')

        # Set the Toast to open
        if cur_id == LayoutMessage.ID_TOAST and cur_prop == 'is_open':
            out[k] = True

        # Set the error message
        if cur_id == LayoutMessage.ID_MESSAGE and cur_prop == 'children':
            out[k] = message

        # Set the exception message
        if cur_id == LayoutMessage.ID_EXCEPTION and cur_prop == 'children':
            if exception is not None:
                out[k] = str(exception)
            else:
                out[k] = ''
    return out
