from flask import request
from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity, jwt_required, jwt_optional
from http import HTTPStatus

from models.workspace import Workspace
from schemas.workspace import WorkspaceSchema

workspace_schema = WorkspaceSchema()


class WorkspaceListResource(Resource):
    """Create new workspace"""

    def post(self):
        """POST -> /workspaces"""
        json_data = request.get_json()
        data, errors = workspace_schema.load(data=json_data)

        if errors:
            return {'message': 'Validation errors', 'errors': errors}, HTTPStatus.BAD_REQUEST

        #if User.get_by_username(data.get('username')):
        #    return {'message': 'username already used'}, HTTPStatus.BAD_REQUEST

        #if User.get_by_email(data.get('email')):
        #    return {'message': 'email already used'}, HTTPStatus.BAD_REQUEST

        workspace = Workspace(**data)
        workspace.save()

        return workspace_schema.dump(workspace).data, HTTPStatus.CREATED
