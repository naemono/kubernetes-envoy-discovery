from marshmallow import Schema, fields


class Host(Schema):
    url = fields.Str()


class Cluster(Schema):
    name = fields.Str()
    type = fields.Str()
    connect_timeout_ms = fields.Int()
    per_connection_buffer_limit_bytes = fields.Int()
    service_name = fields.Str()
    health_check = fields.Dict()
    max_requests_per_connection = fields.Int()
    lb_type = fields.Str()
    features = fields.Str()
    hosts = fields.Nested(Host())


class ClusterManager(Schema):
    clusters = fields.Nested(Cluster())


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
    access_log = fields.Nested(AccessLog, many=True)
    codec_type = fields.String()
    stat_prefix = fields.String()
    route_config = fields.Nested(RouteConfig)
    fields = fields.Nested(Filter)


class Filter(Schema):
    name = fields.String()
    config = fields.Nested(FilterConfig)


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


class ListenerConfiguration(Schema):
    listeners = fields.Nested(Listener())


class Host(Schema):
    ip_address = fields.Str()
    port = fields.Int()
    tags = fields.Dict()


class Service(Schema):
    hosts = fields.Nested(Host())


class BaseFilterSchema(Schema):
    name = fields.Str()
    config = fields.Dict()


class TCPProxyFilterConfig(Schema):
    stat_prefix = fields.String(required=True),
    route_config = fields.Nested(RouteConfig, required=True),
    access_log = fields.Nested(AccessLog, many=True)


class TCPProxyFilter(Schema):
    name = fields.String()
    config = fields.Nested('TCPProxyFilterConfig', required=True)


class MongodbProxyFilterConfig(Schema):
    stat_prefix = fields.String(required=True),
    access_log = fields.String()


class MongodbProxyFilter(Schema):
    name = fields.String()
    config = fields.Nested('MongodbProxyFilterConfig', required=True)


class HTTPConnectionManagerFilterConfig(Schema):
    access_log = fields.Nested(AccessLog()),
    add_user_agent = fields.Bool(),
    codec_type = fields.Str(required=True),
    drain_timeout_ms = fields.Int(),
    filters = fields.Nested(Filter(), required=True),
    generate_request_id = fields.Bool(),
    forward_client_cert = fields.Str(),
    http1_settings = fields.Dict(),
    http2_settings = fields.Dict(),
    idle_timeout_s = fields.Int(),
    rds = fields.Dict(),
    route_config = RouteConfig(),
    server_name = fields.Str(),
    set_current_client_cert = fields.Nested(fields.Str()),
    stat_prefix = fields.Str(required=True),
    tracing = fields.Dict(),
    use_remote_address = fields.Bool(),


class HTTPConnectionManagerFilter(BaseFilterSchema):
    config = HTTPConnectionManagerFilterConfig()
