import logging

import dash
import dash_bootstrap_components as dbc
import dash_cytoscape as cyto
from dash import dcc

from indizio.cache import CACHE_MANAGER
from indizio.components.navbar import NavBar
from indizio.config import RELOAD_ID, TMP_DIR
from indizio.store.clustergram_parameters import ClustergramParametersStore
from indizio.store.distance_matrix import DistanceMatrixStore
from indizio.store.dm_graph import DistanceMatrixGraphStore
from indizio.store.matrix_parameters import MatrixParametersStore
from indizio.store.metadata_file import MetadataFileStore
from indizio.store.network_form_store import NetworkFormStore
from indizio.store.presence_absence import PresenceAbsenceStore
from indizio.store.tree_file import TreeFileStore
from indizio.store.upload_form_store import UploadFormStore
from indizio.util.log import setup_logger
import shutil
# Load extra layouts
cyto.load_extra_layouts()


def main():
    TMP_DIR.mkdir(exist_ok=True)

    try:
        setup_logger()
        log = logging.getLogger()

        log.info(f'Writing temporary files to: {TMP_DIR.as_posix()}')

        # Create the Dash application
        app = dash.Dash(
            __name__,
            use_pages=True,
            suppress_callback_exceptions=True,
            external_stylesheets=[dbc.themes.JOURNAL, dbc.icons.FONT_AWESOME],
            background_callback_manager=CACHE_MANAGER,
        )

        # Create the default layout TODO!
        app.layout = dbc.Container(
            className="container-main",
            fluid=True,
            children=
            [
                # Stores
                NetworkFormStore(),
                UploadFormStore(),
                PresenceAbsenceStore(),
                DistanceMatrixStore(),
                MetadataFileStore(),
                TreeFileStore(),
                DistanceMatrixGraphStore(),
                MatrixParametersStore(),  # todo, add clear?
                ClustergramParametersStore(),

                NavBar(),
                dcc.Location(id=RELOAD_ID, refresh=True),
                dbc.Container(
                    fluid=True,
                    children=
                    [
                        dash.page_container,
                    ]
                )
            ]
        )

        app.run(debug=True, host="0.0.0.0", port=9001)

    finally:
        print('TODO')
        # shutil.rmtree(TMP_DIR.as_posix())


if __name__ == "__main__":
    main()
