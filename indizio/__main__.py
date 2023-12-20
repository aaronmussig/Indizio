import dash
import dash_bootstrap_components as dbc
import dash_cytoscape as cyto
from dash import dcc

from indizio.components.navbar import NavBar
from indizio.config import RELOAD_ID
from indizio.store.distance_matrix import DistanceMatrixFileStore
from indizio.store.dm_graph import DistanceMatrixGraphStore
from indizio.store.matrix_parameters import MatrixParametersStore
from indizio.store.metadata_file import MetadataFileStore
from indizio.store.network_form_store import NetworkFormStore
from indizio.store.presence_absence import PresenceAbsenceFileStore
from indizio.store.tree_file import TreeFileStore
from indizio.store.upload_form_store import UploadFormStore
from indizio.util.log import setup_logger

# Load extra layouts
cyto.load_extra_layouts()


def main():
    setup_logger()

    # Create the Dash application
    app = dash.Dash(
        __name__,
        use_pages=True,
        suppress_callback_exceptions=True,
        external_stylesheets=[dbc.themes.JOURNAL, dbc.icons.FONT_AWESOME],
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
            PresenceAbsenceFileStore(),
            DistanceMatrixFileStore(),
            MetadataFileStore(),
            TreeFileStore(),
            DistanceMatrixGraphStore(),
            MatrixParametersStore(),  # todo, add clear?

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

    app.run(debug=True)


if __name__ == "__main__":
    main()
