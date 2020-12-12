from marshmallow import Schema, fields, post_dump, validate, validates, ValidationError

class WorkspaceSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True, validate=[validate.Length(max=100)])
    user_limit = fields.Integer(required=True)
    available_from = fields.Time(required=True)
    available_till = fields.Time(required=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

    @post_dump(pass_many=True)
    def wrap(self, data, many, **kwargs):
        if many:
            return {"data": data}
        return data
    
    @validates('user_limit')
    def validate_user_limit(self, value):
        if value < 1:
            raise ValidationError('User limit can not be less than 1.')

