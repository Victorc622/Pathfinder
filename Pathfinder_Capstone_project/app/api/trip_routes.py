from flask import Blueprint, jsonify, request, abort
from flask_login import login_required, current_user
from app.models import Trip, db

trip_routes = Blueprint('trips', __name__)

@trip_routes.route('/')
@login_required
def all_trips():
    """
    Get all trips created by the current user.
    """
    trips = Trip.query.filter_by(created_by=current_user.id).all()
    return {'trips': [trip.to_dict() for trip in trips]}


@trip_routes.route('/<int:trip_id>')
@login_required
def get_trip(trip_id):
    """
    Get a specific trip by its ID.
    """
    trip = Trip.query.get(trip_id)
    if not trip or trip.created_by != current_user.id:
        abort(404, description="Trip not found")
    return trip.to_dict()


@trip_routes.route('/', methods=['POST'])
@login_required
def create_trip():
    """
    Create a new trip.
    """
    data = request.get_json()
    trip = Trip(
        title=data['title'],
        description=data.get('description', ''),
        start_date=data['start_date'],
        end_date=data['end_date'],
        created_by=current_user.id,
        is_public=data.get('is_public', False),
    )
    db.session.add(trip)
    db.session.commit()
    return trip.to_dict(), 201


@trip_routes.route('/<int:trip_id>', methods=['PUT'])
@login_required
def update_trip(trip_id):
    """
    Update a trip.
    """
    trip = Trip.query.get(trip_id)
    if not trip or trip.created_by != current_user.id:
        abort(404, description="Trip not found")

    data = request.get_json()
    trip.title = data.get('title', trip.title)
    trip.description = data.get('description', trip.description)
    trip.start_date = data.get('start_date', trip.start_date)
    trip.end_date = data.get('end_date', trip.end_date)
    trip.is_public = data.get('is_public', trip.is_public)

    db.session.commit()
    return trip.to_dict()


@trip_routes.route('/<int:trip_id>', methods=['DELETE'])
@login_required
def delete_trip(trip_id):
    """
    Delete a trip.
    """
    trip = Trip.query.get(trip_id)
    if not trip or trip.created_by != current_user.id:
        abort(404, description="Trip not found")

    db.session.delete(trip)
    db.session.commit()
    return {'message': 'Trip deleted successfully'}