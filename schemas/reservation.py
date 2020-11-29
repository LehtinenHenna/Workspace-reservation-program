from marshmallow import Schema, fields

class ReservationSchema(Schema):
    id = fields.Integer(dump_only=True)
    start_time = fields.DateTime(required=True)
    end_time = fields.DateTime(required=True)
    workspace_id = fields.Integer()
    user_id = fields.Integer()
