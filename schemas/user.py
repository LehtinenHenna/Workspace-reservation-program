from marshmallow import Schema, fields, post_dump
from utils import hash_password

class UserSchema(Schema):
    class Meta:
        ordered = True
    id = fields.Integer(dump_only=True)
    username = fields.String(required=True)
    email = fields.Email(required=True)
    password = fields.Method(required=True, deserialize='load_password')
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

    @post_dump(pass_many=True)
    def wrap(self, data, many, **kwargs):
        if many:
            return {"data": data}
        return data
    
    def load_password(self, value):
        return hash_password(value) 