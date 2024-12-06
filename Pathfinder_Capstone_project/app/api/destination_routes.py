from flask import Blueprint, request, jsonify
from app.models import Destination, Itinerary, db
from flask_login import current_user, login_required

destination_routes = Blueprint('destinations', __name__)

# Get destinations for a specific itinerary
@destination_routes.route('/itinerary/<int:itinerary_id>', methods=['GET'])
@login_required
def get_destinations(itinerary_id):
    try:
        # Validate if the itinerary belongs to the current user
        itinerary = Itinerary.query.get(itinerary_id)
        if not itinerary or itinerary.user_id != current_user.id:
            return jsonify({'error': 'Itinerary not found or unauthorized'}), 404
        
        destinations = Destination.query.filter_by(itinerary_id=itinerary_id).all()
        return jsonify([destination.to_dict() for destination in destinations]), 200
    except Exception as e:
        return jsonify({'error': f'Failed to fetch destinations: {str(e)}'}), 500

# Add a destination to an itinerary
@destination_routes.route('/', methods=['POST'])
@login_required
def create_destination():
    if not request.is_json:
        return jsonify({'error': 'Invalid content type, expected JSON'}), 400

    data = request.json
    try:
        itinerary = Itinerary.query.get(data.get('itinerary_id'))
        if not itinerary or itinerary.user_id != current_user.id:
            return jsonify({'error': 'Itinerary not found or unauthorized'}), 404
        
        if not data.get('name'):
            return jsonify({'error': 'Name is required'}), 400

        new_destination = Destination(
            itinerary_id=data['itinerary_id'],
            name=data['name'],
            description=data.get('description', ''),
            image=data.get('image', None)
        )
        db.session.add(new_destination)
        db.session.commit()
        return jsonify(new_destination.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to create destination: {str(e)}'}), 500

# Update a destination
@destination_routes.route('/<int:id>', methods=['PUT'])
@login_required
def update_destination(id):
    if not request.is_json:
        return jsonify({'error': 'Invalid content type, expected JSON'}), 400

    data = request.json
    try:
        destination = Destination.query.get(id)
        if not destination:
            return jsonify({'error': 'Destination not found'}), 404

        itinerary = Itinerary.query.get(destination.itinerary_id)
        if not itinerary or itinerary.user_id != current_user.id:
            return jsonify({'error': 'Unauthorized'}), 403

        destination.name = data.get('name', destination.name)
        destination.description = data.get('description', destination.description)
        destination.image = data.get('image', destination.image)
        db.session.commit()
        return jsonify(destination.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to update destination: {str(e)}'}), 500

# Delete a destination
@destination_routes.route('/<int:id>', methods=['DELETE'])
@login_required
def delete_destination(id):
    try:
        destination = Destination.query.get(id)
        if not destination:
            return jsonify({'error': 'Destination not found'}), 404

        itinerary = Itinerary.query.get(destination.itinerary_id)
        if not itinerary or itinerary.user_id != current_user.id:
            return jsonify({'error': 'Unauthorized'}), 403

        db.session.delete(destination)
        db.session.commit()
        return jsonify({'message': 'Destination deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to delete destination: {str(e)}'}), 500