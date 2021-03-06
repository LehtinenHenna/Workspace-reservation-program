from flask import request
from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity, jwt_required, jwt_optional
from http import HTTPStatus
import datetime

from models.reservation import Reservation
from models.user import User
from schemas.reservation import ReservationSchema

reservation_schema = ReservationSchema()
reservation_list_schema = ReservationSchema(many=True)


class ReservationListResource(Resource):


    @jwt_required
    def post(self):
        """Create new reservation
        POST -> /reservations"""
        json_data = request.get_json()
        data, errors = reservation_schema.load(data=json_data)

        current_user = get_jwt_identity()     # check who is the logged in user. get_jwt_identity() returns username.

        if errors:
            return {'message': 'Validation errors', 'errors': errors}, HTTPStatus.BAD_REQUEST

        if data.get('end_time') < datetime.datetime.now():     # if the ending time of the reservation is in the past the whole reservation is in the past
            return {'message': 'Reservation time cannot be in the past'}, HTTPStatus.BAD_REQUEST
        
        if data.get('start_time').hour < 16 or data.get('end_time').hour > 21:  # the reservations can only be made between 16 and 21 o'clock
            return {'message': 'Reservations can only be made between 16:00 and 21:00'}, HTTPStatus.BAD_REQUEST

        workspace_id = data.get('workspace_id')
        meetingcollisions = Reservation.get_all_reservations_by_workspace_id(workspace_id=workspace_id)    # all the reservations made to the same workspace
        book_start_time = data.get('start_time')  #start time user wants to book
        book_end_time = data.get('end_time')  #end time user wants to book

        for reserv in meetingcollisions:    # let's check that there's no overlapping reservations to the same workspace
            # [a, b] overlaps with [x, y] if b > x and a < y
            if reserv.end_time > book_start_time and reserv.start_time < book_end_time:     # the reservation works but iteration is throwing an error
                return {'message': 'The selected meeting room is already booked at that time.'}, HTTPStatus.BAD_REQUEST


        reservation = Reservation(**data)
        reservation.username = current_user
        reservation.save()

        return reservation_list_schema.dump(reservation).data, HTTPStatus.CREATED

    
    @jwt_required
    def get(self):
        """ Get all reservations
         GET -> /reservations""" 

        current_user = get_jwt_identity()

        reservations = Reservation.get_all_reservations()

        now = datetime.datetime.now()
        future_reservations = []

        for reservation in reservations:
            if reservation.start_time > now:
                future_reservations.append(reservation)

        return reservation_list_schema.dump(future_reservations).data, HTTPStatus.OK


class ReservationWorkspaceResource(Resource):
    
    @jwt_required
    def get(self, workspace_id):
        """ Get reservations by workspace id
        GET -> /reservations/<int:workspace_id>"""

        reservations = Reservation.get_all_reservations_by_workspace_id(workspace_id=workspace_id)

        now = datetime.datetime.now()

        future_reservations = []

        for reservation in reservations:
            if reservation.start_time > now:
                future_reservations.append(reservation)

        return reservation_list_schema.dump(future_reservations).data, HTTPStatus.OK

class ReservationResource(Resource):

    @jwt_required
    def delete(self, reservation_id):
        """ delete reservation by reservation id
        DELETE -> /reservations/<int:reservation_id>"""

        reservation = Reservation.get_by_id(reservation_id=reservation_id)

        if reservation is None:
            return {'message': 'Reservation not found'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()

        if current_user != reservation.username:
            return {'message': 'Access is not allowed'}, HTTPStatus.FORBIDDEN
        
        reservation.delete()

        return {}, HTTPStatus.NO_CONTENT

class ReservationMeResource(Resource):

    @jwt_required
    def get(self):
        """ Get user's own reservations
         GET -> /reservations/me""" 

        current_user = get_jwt_identity()

        reservations = Reservation.get_all_by_user(username=current_user)

        now = datetime.datetime.now()
        future_reservations = []

        for reservation in reservations:
            if reservation.start_time > now:
                future_reservations.append(reservation)

        return reservation_list_schema.dump(future_reservations).data, HTTPStatus.OK