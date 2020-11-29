from flask import request
from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity, jwt_required, jwt_optional
from http import HTTPStatus
from webargs import fields
from webargs.flaskparser import use_kwargs
from models.user import User
from schemas.user import UserSchema

user_schema = UserSchema()
#recipe_list_schema = RecipeSchema(many=True)
#user_public_schema = UserSchema(exclude=('email', ))


class UserListResource(Resource):
    """Create new user"""

    def post(self):
        """POST -> /users"""
        json_data = request.get_json()
        data, errors = user_schema.load(data=json_data)

        if errors:
            return {'message': 'Validation errors', 'errors': errors}, HTTPStatus.BAD_REQUEST

        if User.get_by_username(data.get('username')):
            return {'message': 'username already used'}, HTTPStatus.BAD_REQUEST

        if User.get_by_email(data.get('email')):
            return {'message': 'email already used'}, HTTPStatus.BAD_REQUEST

        user = User(**data)
        user.save()

        return user_schema.dump(user).data, HTTPStatus.CREATED


class UserResource(Resource):
    """Get user information by username"""

    @jwt_optional
    def get(self, username):

        user = User.get_by_username(username=username)

        if user is None:
            return {'message': 'User not found'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()

        if current_user == user.id:
            data = user_schema.dump(user).data
        else:
            data = user_public_schema.dump(user).data

        return data, HTTPStatus.OK


class MeResource(Resource):
    """Get user information by login"""
    
    @jwt_required
    def get(self):
        user = User.get_by_id(id=get_jwt_identity())

        return user_schema.dump(user).data, HTTPStatus.OK
