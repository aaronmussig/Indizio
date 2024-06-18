import tempfile
from pathlib import Path

# The page title used in displaying the application name.
PAGE_TITLE = 'Indizio'

# Data retention policy for Dash stores.
# memory - Reset of page refresh.
# local - Data is kept indefinetely within the browser.
# session - Kept on page reload, but cleared when the browser is closed.
PERSISTENCE_TYPE = 'session'

# This is a universally unique ID that allows for a full refresh of the page.
RELOAD_ID = 'reload-loc'

# The temporary directory is used to store files that are uploaded.
TMP_DIR = Path(tempfile.gettempdir()) / 'indizio'

# Functions that support Memoization will use this flag to write to disk.
ENABLE_CACHE = True

# Identifiers for some components where a circular import would otherwise be created.
ID_MATRIX_PARAMS_METRIC = 'matrix-params-metric'
ID_CLUSTERGRAM_PARAMS_METRIC = 'clustergram-params-metric'
ID_NETWORK_VIZ_PROGRESS = 'network-viz-progress-bar'
ID_NETWORK_FORM_DEGREE = 'network-form-degree'
ID_NETWORK_FORM_DEGREE_LOWER_VALUE = f'{ID_NETWORK_FORM_DEGREE}-lower-value'
ID_NETWORK_FORM_DEGREE_UPPER_VALUE = f'{ID_NETWORK_FORM_DEGREE}-upper-value'
ID_NETWORK_FORM_EDGES_TO_SELF = f'{ID_NETWORK_FORM_DEGREE}-show-edges-to-self'

ID_NETWORK_VIZ_EDGE_COUNT = 'network-viz-edge-count'
ID_NETWORK_VIZ_NODE_COUNT = 'network-viz-node-count'
ID_NETWORK_VIZ_FILTERING_APPLIED = 'network-viz-filtering-applied'

ID_NETWORK_FORM_NODE_METADATA_COLOR_FILE = 'network-form-node-metadata-color-file'
ID_NETWORK_FORM_NODE_METADATA_COLOR_COLUMN = 'network-form-node-metadata-color-column'
ID_NETWORK_FORM_NODE_METADATA_SIZE_FILE = 'network-form-node-metadata-size-file'
ID_NETWORK_FORM_NODE_METADATA_SIZE_COLUMN = 'network-form-node-metadata-size-column'


ID_NETWORK_PARAM_EDGE_WEIGHTS = 'network-parameters-edge-weights'
ID_NETWORK_PARAM_METRIC_SELECT = 'network-parameters-metric-select'


GRAPH_AXIS_FONT_SIZE = 10
GRAPH_AXIS_MAX_LENGTH = 10
