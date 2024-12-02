from flask import Blueprint, request, jsonify
from app.models import Destination, Itinerary, db
from flask_login import current_user, login_required

destination_routes = Blueprint('destinations', __name__)

# Get destinations for a specific itinerary
@destination_routes.route('/itinerary/<int:itinerary_id>')
@login_required
def get_destinations(itinerary_id):
    destinations = Destination.query.filter_by(itinerary_id=itinerary_id).all()
    return jsonify([destination.to_dict() for destination in destinations])

# Add a destination to an itinerary
@destination_routes.route('/', methods=['POST'])
@login_required
def create_destination():
    data = request.json
    itinerary = Itinerary.query.get(data['itinerary_id'])
    if not itinerary or itinerary.user_id != current_user.id:
        return jsonify({'error': 'Itinerary not found or unauthorized'}), 404
    new_destination = Destination(
        itinerary_id=data['itinerary_id'],
        name=data['name'],
        description=data.get('description', '')
    )
    db.session.add(new_destination)
    db.session.commit()
    return jsonify(new_destination.to_dict())

# Update a destination
@destination_routes.route('/<int:id>', methods=['PUT'])
@login_required
def update_destination(id):
    data = request.json
    destination = Destination.query.get(id)
    if not destination:
        return jsonify({'error': 'Destination not found'}), 404
    destination.name = data.get('name', destination.name)
    destination.description = data.get('description', destination.description)
    db.session.commit()
    return jsonify(destination.to_dict())

# Delete a destination
@destination_routes.route('/<int:id>', methods=['DELETE'])
@login_required
def delete_destination(id):
    destination = Destination.query.get(id)
    if not destination:
        return jsonify({'error': 'Destination not found'}), 404
    db.session.delete(destination)
    db.session.commit()
    return jsonify({'message': 'Destination deleted successfully'})