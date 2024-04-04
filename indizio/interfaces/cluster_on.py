from indizio.interfaces.html_option import HtmlOption


class ClusterOn(HtmlOption):
    """
    This class is used to represent the options for the clustering on.
    """

    NOTHING = 'No clustering'
    FEATURES = 'Features'
    IDS = 'Identifiers'
    BOTH = 'Features & Identifiers'

    def is_identifiers(self) -> bool:
        return self is ClusterOn.IDS or self is ClusterOn.BOTH

    def is_features(self) -> bool:
        return self is ClusterOn.FEATURES or self is ClusterOn.BOTH
