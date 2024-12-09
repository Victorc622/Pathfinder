from flask import Blueprint, request, jsonify
from app.models import Destination, Itinerary, db
from flask_login import current_user, login_required

destination_routes = Blueprint('destinations', __name__)

@destination_routes.route('/itinerary/<int:itinerary_id>', methods=['GET'])
@login_required
def get_destinations(itinerary_id):
    try:
        itinerary = Itinerary.query.get(itinerary_id)
        if not itinerary or itinerary.user_id != current_user.id:
            return jsonify({'error': 'Itinerary not found or unauthorized'}), 404

        destinations = Destination.query.filter_by(itinerary_id=itinerary_id).all()
        return jsonify([destination.to_dict() for destination in destinations]), 200
    except Exception as e:
        return jsonify({'error': f'Failed to fetch destinations: {str(e)}'}), 500

@destination_routes.route('/', methods=['GET'])
@login_required
def get_all_destinations():
    try:
        default_itinerary = Itinerary.query.filter_by(user_id=current_user.id).first()
        if not default_itinerary:
            return jsonify({'error': 'No itineraries found'}), 404

        destinations = Destination.query.filter_by(itinerary_id=default_itinerary.id).all()
        return jsonify([destination.to_dict() for destination in destinations]), 200
    except Exception as e:
        return jsonify({'error': f'Failed to fetch destinations: {str(e)}'}), 500

@destination_routes.route('/', methods=['POST'])
@login_required
def create_destination():
    if not request.is_json:
        return jsonify({'error': 'Invalid content type, expected JSON'}), 400

    data = request.json
    try:
        itinerary = Itinerary.query.get(data.get('itinerary_id'))
        if not itinerary or itinerary.user_id != current_user.id:
            return jsonify({'error': 'Unauthorized or itinerary not found'}), 403

        destination = Destination(
            name=data.get('name'),
            description=data.get('description'),
            itinerary_id=itinerary.id
        )
        db.session.add(destination)
        db.session.commit()

        return jsonify(destination.to_dict()), 201
    except Exception as e:
        return jsonify({'error': f'Failed to create destination: {str(e)}'}), 500
    
@destination_routes.route('/<int:destination_id>', methods=['DELETE'])
@login_required
def delete_destination(destination_id):
    """
    Deletes a destination if the user is authorized to do so.
    """
    try:
        
        destination = Destination.query.get(destination_id)
        if not destination:
            return jsonify({'error': 'Destination not found'}), 404

        itinerary = Itinerary.query.get(destination.itinerary_id)
        if not itinerary or itinerary.user_id != current_user.id:
            return jsonify({'error': 'Unauthorized or itinerary not found'}), 403

        db.session.delete(destination)
        db.session.commit()

        return jsonify({'message': 'Destination deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to delete destination: {str(e)}'}), 500
    
@destination_routes.route('/<int:destination_id>', methods=['PUT'])
@login_required
def update_destination(destination_id):
    """
    Updates a destination if the user is authorized to do so.
    """
    if not request.is_json:
        return jsonify({'error': 'Invalid content type, expected JSON'}), 400

    data = request.json
    try:
    
        destination = Destination.query.get(destination_id)
        if not destination:
            return jsonify({'error': 'Destination not found'}), 404

    
        itinerary = Itinerary.query.get(destination.itinerary_id)
        if not itinerary or itinerary.user_id != current_user.id:
            return jsonify({'error': 'Unauthorized or itinerary not found'}), 403

    
        destination.name = data.get('name', destination.name)
        destination.description = data.get('description', destination.description)

        db.session.commit()

        return jsonify(destination.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to update destination: {str(e)}'}), 500
