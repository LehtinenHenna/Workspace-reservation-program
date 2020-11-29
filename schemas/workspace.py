from marshmallow import Schema, fields

class WorkspaceSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True)
    user_limit = fields.Integer()
    available_from = fields.Time(16)
    available_till = fields.Time(21)
