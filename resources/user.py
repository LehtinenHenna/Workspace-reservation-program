from flask import request
from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity, jwt_required, jwt_optional
from http import HTTPStatus
from webargs import fields
from webargs.flaskparser import use_kwargs
from models.user import User
from schemas.user import UserSchema

user_schema = UserSchema()
user_public_schema = UserSchema(exclude=('email', ))
#recipe_list_schema = RecipeSchema(many=True)


class UserListResource(Resource):
    """Create new user. Require admin rights."""

    @jwt_required
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

        current_user = get_jwt_identity()

        if current_user == "admin":
            user = User(**data)
            user.save()
            return user_schema.dump(user).data, HTTPStatus.CREATED
        else:
            return {"message": "no admin authorization"}, HTTPStatus.FORBIDDEN


class UserResource(Resource):
    """Get user information by username. Require admin rights."""

    @jwt_required
    def get(self, username):
        """GET -> /users/<string:username>"""
        user = User.get_by_username(username=username)

        if user is None:
            return {'message': 'User not found'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()

        if current_user == "admin":
            data = user_schema.dump(user).data
            return data, HTTPStatus.OK
        else:
            return {"message": "no admin authorization"}, HTTPStatus.FORBIDDEN

        


class MeResource(Resource):
    """Get own user information when logged in"""
    
    @jwt_required
    def get(self):
        """GET -> /me"""
        user = User.get_by_username(username=get_jwt_identity())

        return user_schema.dump(user).data, HTTPStatus.OK
