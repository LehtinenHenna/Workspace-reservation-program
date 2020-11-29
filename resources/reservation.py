from flask import request
from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity, jwt_required, jwt_optional
from http import HTTPStatus

from models.reservation import Reservation
from schemas.reservation import ReservationSchema

reservation_schema = ReservationSchema()


class ReservationListResource(Resource):
    """Create new reservation"""

    def post(self):
        """POST -> /reservations"""
        json_data = request.get_json()
        data, errors = reservation_schema.load(data=json_data)

        if errors:
            return {'message': 'Validation errors', 'errors': errors}, HTTPStatus.BAD_REQUEST

        #if User.get_by_username(data.get('username')):
        #    return {'message': 'username already used'}, HTTPStatus.BAD_REQUEST

        #if User.get_by_email(data.get('email')):
        #    return {'message': 'email already used'}, HTTPStatus.BAD_REQUEST

        reservation = Reservation(**data)
        reservation.save()

        return reservation_schema.dump(reservation).data, HTTPStatus.CREATED