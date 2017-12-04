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
