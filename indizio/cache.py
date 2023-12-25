import diskcache
from dash import DiskcacheManager

from indizio.config import TMP_DIR

# So far the diskcache manager only supports monitoring background=True
# processess, I haven't been able to get it to cache execution results.
CACHE = diskcache.Cache(TMP_DIR)
CACHE_MANAGER = DiskcacheManager(
    CACHE,
)
