from flask import Blueprint, jsonify, request, abort
from flask_login import login_required, current_user
from app.models import ItineraryItem, Trip, db

itinerary_item_routes = Blueprint('itinerary_items', __name__)

@itinerary_item_routes.route('/<int:trip_id>/items', methods=['GET'])
@login_required
def get_itinerary_items(trip_id):
    """
    Get all itinerary items for a specific trip.
    """
    trip = Trip.query.get(trip_id)
    if not trip or trip.created_by != current_user.id:
        abort(404, description="Trip not found")

    items = ItineraryItem.query.filter_by(trip_id=trip_id).all()
    return {'itinerary_items': [item.to_dict() for item in items]}


@itinerary_item_routes.route('/<int:trip_id>/items', methods=['POST'])
@login_required
def create_itinerary_item(trip_id):
    """
    Add an itinerary item to a specific trip.
    """
    trip = Trip.query.get(trip_id)
    if not trip or trip.created_by != current_user.id:
        abort(404, description="Trip not found")

    data = request.get_json()
    item = ItineraryItem(
        trip_id=trip_id,
        user_id=current_user.id,
        title=data['title'],
        description=data.get('description', ''),
        start_time=data['start_time'],
        end_time=data['end_time'],
        location=data.get('location', ''),
    )
    db.session.add(item)
    db.session.commit()
    return item.to_dict(), 201


@itinerary_item_routes.route('/<int:item_id>', methods=['PUT'])
@login_required
def update_itinerary_item(item_id):
    """
    Update an itinerary item.
    """
    item = ItineraryItem.query.get(item_id)
    if not item or item.user_id != current_user.id:
        abort(404, description="Item not found")

    data = request.get_json()
    item.title = data.get('title', item.title)
    item.description = data.get('description', item.description)
    item.start_time = data.get('start_time', item.start_time)
    item.end_time = data.get('end_time', item.end_time)
    item.location = data.get('location', item.location)

    db.session.commit()
    return item.to_dict()


@itinerary_item_routes.route('/<int:item_id>', methods=['DELETE'])
@login_required
def delete_itinerary_item(item_id):
    """
    Delete an itinerary item.
    """
    item = ItineraryItem.query.get(item_id)
    if not item or item.user_id != current_user.id:
        abort(404, description="Item not found")

    db.session.delete(item)
    db.session.commit()
    return {'message': 'Item deleted successfully'}