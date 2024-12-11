from flask import Blueprint, jsonify, request, abort
from flask_login import login_required, current_user
from app.models import Destination, Trip, db

destination_routes = Blueprint('destinations', __name__)

@destination_routes.route('/<int:trip_id>', methods=['GET'])
@login_required
def get_destinations(trip_id):
    """
    Get all destinations for a trip.
    """
    trip = Trip.query.get(trip_id)
    if not trip or trip.created_by != current_user.id:
        abort(404, description="Trip not found")

    destinations = Destination.query.filter_by(trip_id=trip_id).all()
    return {'destinations': [dest.to_dict() for dest in destinations]}


@destination_routes.route('/<int:trip_id>', methods=['POST'])
@login_required
def create_destination(trip_id):
    """
    Create a destination for a trip.
    """
    trip = Trip.query.get(trip_id)
    if not trip or trip.created_by != current_user.id:
        abort(404, description="Trip not found")

    data = request.get_json()
    destination = Destination(
        trip_id=trip_id,
        name=data['name'],
        latitude=data.get('latitude'),
        longitude=data.get('longitude'),
        notes=data.get('notes', '')
    )
    db.session.add(destination)
    db.session.commit()
    return destination.to_dict(), 201


@destination_routes.route('/<int:dest_id>', methods=['PUT'])
@login_required
def update_destination(dest_id):
    """
    Edit a destination.
    """
    destination = Destination.query.get(dest_id)
    if not destination or destination.trip.created_by != current_user.id:
        abort(404, description="Destination not found")

    data = request.get_json()
    destination.name = data.get('name', destination.name)
    destination.latitude = data.get('latitude', destination.latitude)
    destination.longitude = data.get('longitude', destination.longitude)
    destination.notes = data.get('notes', destination.notes)

    db.session.commit()
    return destination.to_dict()


@destination_routes.route('/<int:dest_id>', methods=['DELETE'])
@login_required
def delete_destination(dest_id):
    """
    Delete a destination.
    """
    destination = Destination.query.get(dest_id)
    if not destination or destination.trip.created_by != current_user.id:
        abort(404, description="Destination not found")

    db.session.delete(destination)
    db.session.commit()
    return {'message': 'Destination deleted successfully'}