from envoy_listener_discovery import ma
from envoy_listener_discovery.listeners import models


class RouteSchema(ma.Schema):
    class Meta:
        model = models.Route
        # Fields to expose
        fields = ('timeout_ms', 'prefix', 'cluster',)


class VirtualHostSchema(ma.Schema):
    class Meta:
        model = models.VirtualHost
        # Fields to expose
        fields = ('name', 'domains', 'routes',)


class RouteConfigSchema(ma.Schema):
    class Meta:
        model = models.RouteConfig
        # Fields to expose
        fields = ('virtual_hosts',)


class FilterSchema(ma.Schema):
    class Meta:
        model = models.Filter
        # Fields to expose
        fields = ('name', 'config',)


class AccessLogSchema(ma.Schema):
    class Meta:
        model = models.AccessLog
        # Fields to expose
        fields = ('path',)


class FilterConfigSchema(ma.Schema):
    class Meta:
        model = models.FilterConfig
        # Fields to expose
        fields = ('access_log', 'codec_type', 'stat_prefix', 'route_config', 'fields',)


class ListenerSchema(ma.Schema):
    class Meta:
        model = models.Listener
        # Fields to expose
        fields = ('address', 'filters',)


class AdminSchema(ma.Schema):
    class Meta:
        model = models.Admin
        # Fields to expose
        fields = ('access_log_path', 'address',)


class HostSchema(ma.Schema):
    class Meta:
        model = models.Host
        # Fields to expose
        fields = ('url',)


class ClusterSchema(ma.Schema):
    class Meta:
        model = models.Cluster
        # Fields to expose
        fields = ('name', 'connect_timeout_ms', 'type', 'lb_type', 'features', 'hosts',)


class ClusterManagerSchema(ma.Schema):
    class Meta:
        model = models.ClusterManager
        # Fields to expose
        fields = ('clusters',)


class ListenerConfigurationSchema(ma.Schema):
    class Meta:
        model = models.ListenerConfiguration
        # Fields to expose
        fields = ('listeners', 'admin', 'cluster_manager',)
