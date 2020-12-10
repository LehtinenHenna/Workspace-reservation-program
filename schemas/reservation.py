from marshmallow import Schema, fields, post_dump
from schemas.user import UserSchema

class ReservationSchema(Schema):
    id = fields.Integer(dump_only=True)
    start_time = fields.DateTime(required=True)
    end_time = fields.DateTime(required=True)
    workspace_id = fields.Integer()
    username = fields.String(dump_only=True)

    @post_dump(pass_many=True)
    def wrap(self, data, many, **kwargs):
        if many:
            return {"data": data}
        return data