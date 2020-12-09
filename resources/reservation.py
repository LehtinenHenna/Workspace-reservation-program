from flask import request
from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity, jwt_required, jwt_optional
from http import HTTPStatus

from models.reservation import Reservation
from models.user import User
from schemas.reservation import ReservationSchema

reservation_schema = ReservationSchema()


class ReservationListResource(Resource):

    @jwt_required
    def post(self):
        """Create new reservation
        POST -> /reservations"""
        json_data = request.get_json()
        data, errors = reservation_schema.load(data=json_data)

        current_user = get_jwt_identity()     # katsotaan kuka on kirjautunut käyttäjä

        if errors:
            return {'message': 'Validation errors', 'errors': errors}, HTTPStatus.BAD_REQUEST

        #if User.get_by_username(data.get('username')):
        #    return {'message': 'username already used'}, HTTPStatus.BAD_REQUEST

        #if User.get_by_email(data.get('email')):
        #    return {'message': 'email already used'}, HTTPStatus.BAD_REQUEST

        reservation = Reservation(**data)
        reservation.username = current_user
        reservation.save()

        return reservation_schema.dump(reservation).data, HTTPStatus.CREATED

    
    @jwt_required
    def get(self):
        """ Get user's own reservations
         GET -> /reservations""" 

        current_user = get_jwt_identity()

        reservations = Reservation.get_all_by_user(username=current_user)

        return reservation_schema.dump(reservations).data, HTTPStatus.OK