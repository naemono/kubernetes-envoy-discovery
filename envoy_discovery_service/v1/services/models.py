from marshmallow import Schema, fields


class Host(Schema):
    ip_address = fields.Str()
    port = fields.Int()
    tags = fields.Dict()


class Service(Schema):
    hosts = fields.Nested(Host())
