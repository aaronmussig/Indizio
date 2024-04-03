import logging

import dash_bootstrap_components as dbc
from dash import Output, Input, callback
from dash.exceptions import PreventUpdate

from indizio.config import RELOAD_ID
from indizio.store.clustergram_parameters import ClustergramParametersStore
from indizio.store.distance_matrix import DistanceMatrixStore
from indizio.store.dm_graph import DistanceMatrixGraphStore
from indizio.store.matrix_parameters import MatrixParametersStore
from indizio.store.metadata_file import MetadataFileStore
from indizio.store.network_form_store import NetworkFormStore
from indizio.store.network_interaction import NetworkInteractionStore
from indizio.store.presence_absence import PresenceAbsenceStore
from indizio.store.tree_file import TreeFileStore
from indizio.store.upload_form_store import UploadFormStore


class UploadFormBtnClear(dbc.Button):
    """
    This component is the button that triggers the upload and processing of files.
    """

    ID = "upload-form-upload-button-clear"

    def __init__(self):
        super().__init__(
            style={
                'width': '150px',
            },
            className='me-2',
            children=[
                "Reset",
            ],
            id=self.ID,
            color="danger"
        )

        @callback(
            output=dict(
                clustergram_parameters=Output(ClustergramParametersStore.ID, "clear_data"),
                distance_matrix_store=Output(DistanceMatrixStore.ID, "clear_data"),
                dm_graph_store=Output(DistanceMatrixGraphStore.ID, "clear_data"),
                matrix_graph_store=Output(MatrixParametersStore.ID, "clear_data"),
                metadata_store=Output(MetadataFileStore.ID, "clear_data"),
                network_store=Output(NetworkFormStore.ID, "clear_data"),
                network_interaction=Output(NetworkInteractionStore.ID, "clear_data"),
                presence_absence_store=Output(PresenceAbsenceStore.ID, "clear_data"),
                tree_store=Output(TreeFileStore.ID, "clear_data"),
                upload_store=Output(UploadFormStore.ID, "clear_data"),
                reload=Output(RELOAD_ID, "href", allow_duplicate=True),
            ),
            inputs=dict(
                n_clicks=Input(self.ID, "n_clicks"),
            ),
            prevent_initial_call=True
        )
        def reset_state(n_clicks):
            """
            Removes all uploaded files and resets the program.
            """

            # Output debugging information
            log = logging.getLogger()
            if n_clicks is None:
                log.debug(f'{self.ID} - No click was made, updated prevented.')
                raise PreventUpdate
            log.debug(f'{self.ID} - Resetting program to default state.')
            return dict(
                clustergram_parameters=True,
                distance_matrix_store=True,
                dm_graph_store=True,
                matrix_graph_store=True,
                metadata_store=True,
                network_store=True,
                network_interaction=True,
                presence_absence_store=True,
                tree_store=True,
                upload_store=True,
                reload="/"
            )
