from indizio.store.clustergram.parameters import ClustergramParametersStore
from indizio.store.matrix.dm_files import DistanceMatrixStore
from indizio.store.matrix.parameters import MatrixParametersStore
from indizio.store.metadata_file import MetadataFileStore
from indizio.store.network.graph import DistanceMatrixGraphStore
from indizio.store.network.interaction import NetworkInteractionStore
from indizio.store.network.parameters import NetworkFormStore
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
