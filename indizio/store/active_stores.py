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

ACTIVE_STORES = [
    ClustergramParametersStore(),
    DistanceMatrixStore(),
    DistanceMatrixGraphStore(),
    MatrixParametersStore(),
    MetadataFileStore(),
    NetworkFormStore(),
    NetworkInteractionStore(),
    PresenceAbsenceStore(),
    TreeFileStore(),
    UploadFormStore(),
]
