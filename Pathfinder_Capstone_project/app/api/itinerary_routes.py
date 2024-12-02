from flask import Blueprint, request, jsonify
from app.models import Itinerary, db
from flask_login import current_user, login_required

itinerary_routes = Blueprint('itineraries', __name__)

# Get all itineraries for the logged-in user
@itinerary_routes.route('/')
@login_required
def get_itineraries():
    itineraries = Itinerary.query.filter_by(user_id=current_user.id).all()
    return jsonify([itinerary.to_dict() for itinerary in itineraries])

# Create a new itinerary
@itinerary_routes.route('/', methods=['POST'])
@login_required
def create_itinerary():
    data = request.json
    new_itinerary = Itinerary(
        user_id=current_user.id,
        name=data['name'],
        start_date=data['start_date'],
        end_date=data['end_date']
    )
    db.session.add(new_itinerary)
    db.session.commit()
    return jsonify(new_itinerary.to_dict())

# Update an itinerary
@itinerary_routes.route('/<int:id>', methods=['PUT'])
@login_required
def update_itinerary(id):
    data = request.json
    itinerary = Itinerary.query.get(id)
    if not itinerary or itinerary.user_id != current_user.id:
        return jsonify({'error': 'Itinerary not found or unauthorized'}), 404
    itinerary.name = data.get('name', itinerary.name)
    itinerary.start_date = data.get('start_date', itinerary.start_date)
    itinerary.end_date = data.get('end_date', itinerary.end_date)
    db.session.commit()
    return jsonify(itinerary.to_dict())

# Delete an itinerary
@itinerary_routes.route('/<int:id>', methods=['DELETE'])
@login_required
def delete_itinerary(id):
    itinerary = Itinerary.query.get(id)
    if not itinerary or itinerary.user_id != current_user.id:
        return jsonify({'error': 'Itinerary not found or unauthorized'}), 404
    db.session.delete(itinerary)
    db.session.commit()
    return jsonify({'message': 'Itinerary deleted successfully'})