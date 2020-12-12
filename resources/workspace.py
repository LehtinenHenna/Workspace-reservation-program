from flask import request
from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity, jwt_required, jwt_optional
from http import HTTPStatus

from models.workspace import Workspace
from schemas.workspace import WorkspaceSchema

workspace_schema = WorkspaceSchema()
workspace_list_schema = WorkspaceSchema(many=True)


class WorkspaceListResource(Resource):


    @jwt_required
    def post(self):
        """Create new workspace"""
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




    def get(self):
        """Get all workspaces"""
        """GET -> /workspaces"""
        workspaces = Workspace.get_all()
        return workspace_list_schema.dump(workspaces).data, HTTPStatus.OK


class WorkspaceResource(Resource):

    
    def get(self, name):
        """Get specific workspace"""
        """GET -> /workspaces/<string:name>"""
        workspace = Workspace.get_by_name(name=name)
        if workspace is None:
            return {'message': 'Workspace not found'}, HTTPStatus.NOT_FOUND
        return workspace_schema.dump(workspace).data, HTTPStatus.OK


    @jwt_required
    def delete(self, name):
        """Deletes a workspace"""
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
        """Modifies a workspace"""
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
