from flask import Blueprint, request, jsonify
from app.models import Itinerary, Activity, db
from flask_login import current_user, login_required
from datetime import datetime

itinerary_routes = Blueprint('itineraries', __name__)

def validate_date(date_str, format='%m-%d-%Y'):
    try:
        return datetime.strptime(date_str, format).date()
    except ValueError:
        return None

# Get all itineraries for the logged-in user
@itinerary_routes.route('/', methods=['GET'])
@login_required
def get_itineraries():
    itineraries = Itinerary.query.filter_by(user_id=current_user.id).all()
    return jsonify([itinerary.to_dict() for itinerary in itineraries]), 200

# Create a new itinerary with activities
@itinerary_routes.route('/', methods=['POST'])
@login_required
def create_itinerary():
    data = request.json

    name = data.get('name')
    start_date_str = data.get('start_date')
    end_date_str = data.get('end_date')

    if not name or not start_date_str or not end_date_str:
        return jsonify({"error": "Missing required fields"}), 400

    start_date = validate_date(start_date_str)
    end_date = validate_date(end_date_str)

    if not start_date or not end_date:
        return jsonify({"error": "Invalid date format"}), 400

    new_itinerary = Itinerary(
        name=name,
        start_date=start_date,
        end_date=end_date,
        user_id=current_user.id
    )

    db.session.add(new_itinerary)
    db.session.commit()

    return jsonify(new_itinerary.to_dict()), 201

# Get a single itinerary by ID
@itinerary_routes.route('/<int:id>', methods=['GET'])
@login_required
def get_itinerary(id):
    itinerary = Itinerary.query.filter_by(id=id, user_id=current_user.id).first()
    if not itinerary:
        return jsonify({"error": "Itinerary not found"}), 404
    return jsonify(itinerary.to_dict()), 200

# Update an existing itinerary
@itinerary_routes.route('/<int:id>', methods=['PUT'])
@login_required
def update_itinerary(id):
    itinerary = Itinerary.query.filter_by(id=id, user_id=current_user.id).first()

    if not itinerary:
        return jsonify({"error": "Itinerary not found"}), 404

    data = request.json
    name = data.get('name')
    start_date_str = data.get('start_date')
    end_date_str = data.get('end_date')

    if not name or not start_date_str or not end_date_str:
        return jsonify({"error": "Missing required fields"}), 400

    start_date = validate_date(start_date_str)
    end_date = validate_date(end_date_str)

    if not start_date or not end_date:
        return jsonify({"error": "Invalid date format"}), 400

    itinerary.name = name
    itinerary.start_date = start_date
    itinerary.end_date = end_date

    db.session.commit()

    return jsonify(itinerary.to_dict()), 200

# Delete an existing itinerary
@itinerary_routes.route('/<int:id>', methods=['DELETE'])
@login_required
def delete_itinerary(id):
    itinerary = Itinerary.query.filter_by(id=id, user_id=current_user.id).first()

    if not itinerary:
        return jsonify({"error": "Itinerary not found"}), 404

    db.session.delete(itinerary)
    db.session.commit()

    return jsonify({"message": "Itinerary deleted successfully"}), 200