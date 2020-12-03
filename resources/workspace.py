from flask import request
from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity, jwt_required, jwt_optional
from http import HTTPStatus

from models.workspace import Workspace
from schemas.workspace import WorkspaceSchema

workspace_schema = WorkspaceSchema()
workspace_list_schema = WorkspaceSchema(many=True)


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

    """Get all workspaces"""

    def get(self):
        """GET <- /workspeces"""
        workspaces = Workspace.get_all()
        return workspace_list_schema.dump(workspaces).data, HTTPStatus.OK


class WorkspaceResource(Resource):
    """Get specific workspace"""
    
    def get(self, name):
        """GET <- /workspeces/name"""
        workspace = Workspace.get_by_name(name=name)
        if workspace is None:
            return {'message':'Workspace not found'}, HTTPStatus.NOT_FOUND
        return workspace_schema.dump(workspace).data, HTTPStatus.OK

    def put(self, workspace_id):
        """PUT -> /workspaces/workspace_id"""
        json_data = request.get_json()
        workspace = Workspace.get_by_id(workspace_id=workspace_id)
        if workspace is None:
            return {'message':'Workspace not found'}, HTTPStatus.NOT_FOUND
        workspace.name = json_data('name')
        workspace.user_limit = json_data('user_limit')
        workspace.available_from = json_data('available_from')
        workspace.available_till = json_data('available_till')
        workspace.save()
        return workspace.data(), HTTPStatus.OK
    
    def delete(self, workspace_id):
        """DELETE /workspaces/workspace_id"""
        workspace = Workspace.get_by_id(workspace_id=workspace_id)
        if workspace is None:
            return {'message':'Workspace not found'}, HTTPStatus.NOT_FOUND
        workspace.delete()
        return {}, HTTPStatus.NO_CONTENT
