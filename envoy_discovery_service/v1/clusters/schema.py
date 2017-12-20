from envoy_discovery_service import ma
from .. import models


class ClusterSchema(ma.Schema):
    class Meta:
        model = models.Cluster
        # Fields to expose
        fields = (
            'name',
            'connect_timeout_ms',
            'type',
            'lb_type',
            'features',
            'hosts',
        )


class ClusterManagerSchema(ma.Schema):
    class Meta:
        model = models.ClusterManager
        # Fields to expose
        fields = ('clusters',)
