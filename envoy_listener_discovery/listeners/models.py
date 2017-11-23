from marshmallow import Schema, fields


class Route(Schema):
    timeout_ms = fields.Int()
    prefix = fields.Str()
    cluster = fields.Str()


class VirtualHost(Schema):
    name = fields.Str()
    domains = fields.List(fields.Str())
    routes = fields.Nested(Route())


class RouteConfig(Schema):
    virtual_hosts = fields.Nested(VirtualHost())


class Filter(Schema):
    name = fields.Str()
    config = fields.Dict()


class AccessLog(Schema):
    path = fields.Str()


class FilterConfig(Schema):
    access_log = fields.Nested(AccessLog())
    codec_type = fields.Str()
    stat_prefix = fields.Str()
    route_config = RouteConfig()
    fields = fields.Nested(Filter())


class Filter(Schema):
    name = fields.Str()
    config = FilterConfig()


class Listener(Schema):
    address = fields.Str()
    filters = fields.Nested(Filter())


class Admin(Schema):
    access_log_path = fields.Str()
    address = fields.Str()


class Host(Schema):
    url = fields.Str()


class Cluster(Schema):
    name = fields.Str()
    connect_timeout_ms = fields.Int()
    type = fields.Str()
    lb_type = fields.Str()
    features = fields.Str()
    hosts = fields.Nested(Host())


class ClusterManager(Schema):
    clusters = fields.Nested(Cluster())


class ListenerConfiguration(Schema):
    listeners = fields.Nested(Listener())
    admin = Admin()
    cluster_manager = ClusterManager()
