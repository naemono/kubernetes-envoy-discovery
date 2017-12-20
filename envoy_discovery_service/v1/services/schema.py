from envoy_discovery_service import ma
from .. import models


class HostSchema(ma.Schema):
    class Meta:
        model = models.Host
        # Fields to expose
        fields = (
            'ip_addressad',
            'port',
            'tags',
        )


class ServiceSchema(ma.Schema):
    class Meta:
        model = models.Service
        # Fields to expose
        fields = ('hosts',)
