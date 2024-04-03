import dash_bootstrap_components as dbc
import logging

from dash import Output, Input, callback, State, ALL, ctx
from dash.exceptions import PreventUpdate

from indizio.components.upload_form.file_selector import UploadFormFileSelector
from indizio.config import RELOAD_ID
from indizio.interfaces.bound import Bound
from indizio.interfaces.file_type import UserFileType
from indizio.store.distance_matrix import DistanceMatrixStore, DistanceMatrixFile, DistanceMatrixData
from indizio.store.dm_graph import DmGraph, DistanceMatrixGraphStore
from indizio.store.metadata_file import MetadataFile, MetadataFileStore, MetadataData
from indizio.store.network_form_store import NetworkFormStore, NetworkFormStoreData, NetworkParamThreshold
from indizio.store.presence_absence import PresenceAbsenceStore, PresenceAbsenceFile, PresenceAbsenceData
from indizio.store.tree_file import TreeFile, TreeFileStore, TreeData
from indizio.store.upload_form_store import UploadFormStore, UploadFormData
from indizio.util.types import ProgressFn


class NavBar(dbc.NavbarSimple):

    ID = 'navbar-container'
    ID_MATRIX = f'{ID}-matrix'
    ID_VIZ = f'{ID}-viz'
    ID_STATS = f'{ID}-stats'

    def __init__(self):
        super().__init__(
            brand='Indizio',
            brand_href='/',
            color="primary",
            dark=True,
            children=[
                dbc.NavItem(dbc.NavLink(
                    "Matrices",
                    href="/matrix",
                    disabled=False,
                    id=self.ID_MATRIX
                )),
                dbc.NavItem(dbc.NavLink(
                    "Network Visualization",
                    href="/network",
                    id=self.ID_VIZ
                )),
                dbc.NavItem(dbc.NavLink(
                    "Network Statistics",
                    href="/stats",
                    id=self.ID_STATS
                )),
            ])

        @callback(
            output=dict(
                matrix=Output(self.ID_MATRIX, 'disabled'),
                viz=Output(self.ID_VIZ, 'disabled'),
                stats=Output(self.ID_STATS, 'disabled')
            ),
            inputs=dict(
                state_dm=Input(DistanceMatrixStore.ID, 'data'),
            ),
        )
        def toggle_nav_disabled(state_dm):
            disabled = not state_dm
            return dict(
                matrix=disabled,
                viz=disabled,
                stats=disabled
            )

