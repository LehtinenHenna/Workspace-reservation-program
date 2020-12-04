from flask import request
from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity, jwt_required, jwt_optional
from http import HTTPStatus
from webargs import fields
from webargs.flaskparser import use_kwargs
from models.user import User
from schemas.user import UserSchema
from utils import check_password, hash_password

user_schema = UserSchema()
user_list_schema = UserSchema(many=True)
user_public_schema = UserSchema(exclude=('email', ))


class UserListResource(Resource):
    """User accounts list methods."""

    def post(self):
        """Create new user: POST -> /users"""
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

    @jwt_required
    def get(self):
        """Get all user accounts: GET -> /users. Require admin."""
        current_user = get_jwt_identity()

        if current_user == "admin":
            users = User.get_all_users()
            data = user_list_schema.dump(users).data
            return data, HTTPStatus.OK
        else:
            return {"message": "no admin authorization"}, HTTPStatus.FORBIDDEN


class UserResource(Resource):
    """Individual username based user account methods. Require admin rights."""

    @jwt_required
    def get(self, username):
        """Get user account information by username: GET -> /users/<string:username>"""
        user = User.get_by_username(username=username)

        if user is None:
            return {'message': 'User not found'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()

        if current_user == "admin":
            data = user_schema.dump(user).data
            return data, HTTPStatus.OK
        else:
            return {"message": "no admin authorization"}, HTTPStatus.FORBIDDEN

    @jwt_required
    def patch(self, username):
        """Modify user account info by username: PATCH -> /users/<string:username>"""
        json_data = request.get_json()

        data, errors = user_schema.load(data=json_data, partial=("username", "email", "password"))

        if errors:
            return {"message": "Validation errors", "errors": errors}, HTTPStatus.BAD_REQUEST

        user = User.get_by_username(username=username)

        if user is None:
            return {"message": "User not found"}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()

        if current_user == "admin":
            user.username = data.get("username") or user.username
            user.email = data.get("email") or user.email
            user.password = user.password #password vaihto ei toimi oikein hashien kanssa

            user.save()

            return user_schema.dump(user).data, HTTPStatus.OK
        else:
            return {"message": "no admin authorization"}, HTTPStatus.FORBIDDEN

    @jwt_required
    def delete(self, username):
        """Delete user account by username: DELETE -> /users/<string:username>"""
        user = User.get_by_username(username=username)

        if user is None:
            return {'message': 'User not found'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()

        if current_user == "admin":
            user.delete()
            return {"message": "deleted user {} succesfully".format(user.username)}, HTTPStatus.OK
        else:
            return {"message": "no admin authorization"}, HTTPStatus.FORBIDDEN    


class MeResource(Resource):
    """Personal user account methods"""
    
    @jwt_required
    def get(self):
        """Get own user account information: GET -> /me"""
        user = User.get_by_username(username=get_jwt_identity())

        return user_schema.dump(user).data, HTTPStatus.OK

    @jwt_required
    def patch(self):
        """Modify own user account info: PATCH -> /me/"""
        json_data = request.get_json()

        data, errors = user_schema.load(data=json_data, partial=("username", "email", "password"))

        if errors:
            return {"message": "Validation errors", "errors": errors}, HTTPStatus.BAD_REQUEST

        user = User.get_by_username(username=get_jwt_identity())

        if user is None:
            return {"message": "User not found"}, HTTPStatus.NOT_FOUND

        user.username = data.get("username") or user.username
        user.email = data.get("email") or user.email
        user.password = user.password #password vaihto ei toimi oikein hashien kanssa

        user.save()

        return user_schema.dump(user).data, HTTPStatus.OK

    @jwt_required
    def delete(self):
        """Delete own user account: DELETE -> /me"""
        user = User.get_by_username(username=get_jwt_identity())

        if user is None:
            return {"message": "user not found"}, HTTPStatus.NOT_FOUND

        user.delete()

        return {"message": "deleted user {} succesfully".format(user.username)}, HTTPStatus.OK
