import tempfile
from pathlib import Path

# The page title used in displaying the application name.
PAGE_TITLE = 'Indizio'

# Data retention policy for Dash stores and input fields.
# memory - Reset of page refresh.
# local - Data is kept indefinetely within the browser.
# session - Kept on page reload, but cleared when the browser is closed.
PERSISTENCE_TYPE = 'session'

# This is a universally unique ID that allows for a full refresh of the page.
RELOAD_ID = 'reload-loc'

# TODO: Remove?
CONSOLE_REFRESH_MS = 1000

# The temporary directory is used to store files that are uploaded.
TMP_DIR = Path(tempfile.gettempdir()) / 'indizio'

# Identifiers for some components where a circular import would otherwise be created
ID_MATRIX_PARAMS_METRIC = 'matrix-params-metric'
ID_CLUSTERGRAM_PARAMS_METRIC = 'clustergram-params-metric'
ID_NETWORK_VIZ_PROGRESS = 'network-viz-progress-bar'
ID_NETWORK_FORM_DEGREE = 'network-form-degree'
ID_NETWORK_FORM_DEGREE_LOWER_VALUE = f'{ID_NETWORK_FORM_DEGREE}-lower-value'
ID_NETWORK_FORM_DEGREE_UPPER_VALUE = f'{ID_NETWORK_FORM_DEGREE}-upper-value'
ID_NETWORK_FORM_EDGES_TO_SELF = f'{ID_NETWORK_FORM_DEGREE}-show-edges-to-self'

ID_NETWORK_VIZ_NODE_EDGE_COUNT = 'network-viz-node-edge-count'

ENABLE_CACHE = True
