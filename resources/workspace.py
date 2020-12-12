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

    @jwt_required
    def post(self):
        """POST -> /workspaces"""
        json_data = request.get_json()
        data, errors = workspace_schema.load(data=json_data)

        current_user = get_jwt_identity()

        if current_user == "admin":
            if errors:
                return {'message': 'Validation errors', 'errors': errors}, HTTPStatus.BAD_REQUEST
            if Workspace.get_by_name(data.get('name')):
                return {'message': 'Workspace name already used'}, HTTPStatus.BAD_REQUEST
            else:
                workspace = Workspace(**data)
                workspace.save()
                return workspace_schema.dump(workspace).data, HTTPStatus.CREATED

        else:
            return {"message": "no admin authorization"}, HTTPStatus.FORBIDDEN



    """Get all workspaces"""

    def get(self):
        """GET <- /workspeces"""
        workspaces = Workspace.get_all()
        return workspace_list_schema.dump(workspaces).data, HTTPStatus.OK


class WorkspaceResource(Resource):
    """Get specific workspace"""
    
    def get(self, name):
        """GET <- /workspaces/<string:name>"""
        workspace = Workspace.get_by_name(name=name)
        if workspace is None:
            return {'message': 'Workspace not found'}, HTTPStatus.NOT_FOUND
        return workspace_schema.dump(workspace).data, HTTPStatus.OK

    @jwt_required
    def put(self, name):
        """PUT -> /workspaces/<string:name>"""
        json_data = request.get_json()
        workspace = Workspace.get_by_name(name=name)

        current_user = get_jwt_identity()

        if current_user == "admin":
            if workspace is None:
                return {'message': 'Workspace not found'}, HTTPStatus.NOT_FOUND
            else:
                workspace.name = json_data['name']
                workspace.user_limit = json_data['user_limit']
                workspace.available_from = json_data['available_from']
                workspace.available_till = json_data['available_till']
                workspace.save()
                return workspace.data(), HTTPStatus.OK

        else:
            return {"message": "no admin authorization"}, HTTPStatus.FORBIDDEN

    @jwt_required
    def delete(self, name):
        """DELETE /workspaces/<string:name>"""
        workspace = Workspace.get_by_name(name=name)

        current_user = get_jwt_identity()

        if current_user == "admin":
            if workspace is None:
                return {'message': 'Workspace not found'}, HTTPStatus.NOT_FOUND
            else:
                workspace.delete()
                return {}, HTTPStatus.NO_CONTENT

        else:
            return {"message": "no admin authorization"}, HTTPStatus.FORBIDDEN

    @jwt_required
    def patch(self, name):
        """PATCH -> /workspaces/<string:name>"""
        json_data = request.get_json()
        data, errors = workspace_schema.load(data=json_data, partial=('name',))

        current_user = get_jwt_identity()

        if current_user == "admin":
            if errors:
                return {'message': 'Validation errors', 'errors': errors}, HTTPStatus.BAD_REQUEST

            workspace = Workspace.get_by_name(name=name)
            if workspace is None:
                return {'message': 'Workspace not found'}, HTTPStatus.NOT_FOUND
            else:
                workspace.name = data.get('name') or workspace.name
                workspace.user_limit = data.get('user_limit') or workspace.user_limit
                workspace.available_from = data.get('available_from') or workspace.available_from
                workspace.available_till = data.get('available_till') or workspace.available_till
                workspace.save()
                return workspace_schema.dump(workspace).data, HTTPStatus.OK
        else:
            return {"message": "no admin authorization"}, HTTPStatus.FORBIDDEN
