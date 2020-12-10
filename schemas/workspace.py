from marshmallow import Schema, fields, post_dump, validate, validates, ValidationError

class WorkspaceSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True)
    user_limit = fields.Integer()
    available_from = fields.Time(16)
    available_till = fields.Time(21)

    @post_dump(pass_many=True)
    def wrap(self, data, many, **kwargs):
        if many:
            return {"data": data}
        return data
    
    @validates('user_limit')
    def validate_user_limit(self, value):
        if value < 1:
            raise ValidationError('User limit can not be less than 1.')

    @validates('available_from')
    def validate_available_from(self, value):
        if value < 16:
            raise ValidationError('Available from must be greater than or equal to 16.')
        if value > 20:
            raise ValidationError('Available from must be less than 21.')

    @validates('available_till')
    def validate_available_till(self, value):
        if value > 21:
            raise ValidationError('Available till must be less than or equal to 21.')
        if value < 17:
            raise ValidationError('Available till mus be greater than 16.')
