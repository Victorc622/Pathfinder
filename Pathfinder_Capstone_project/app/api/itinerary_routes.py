from flask import Blueprint, request, jsonify
from app.models import Itinerary, Activity, db
from flask_login import current_user, login_required
from datetime import datetime

itinerary_routes = Blueprint('itineraries', __name__)

# Get all itineraries for the logged-in user
@itinerary_routes.route('/')
@login_required
def get_itineraries():
    itineraries = Itinerary.query.filter_by(user_id=current_user.id).all()
    return jsonify([itinerary.to_dict() for itinerary in itineraries]), 200

# Create a new itinerary with activities
@itinerary_routes.route('/', methods=['POST'])
@login_required
def create_itinerary():
    data = request.json

    # Validate input data
    if not data.get('name') or not data.get('start_date') or not data.get('end_date'):
        return jsonify({'error': 'Missing required fields: name, start_date, or end_date'}), 400

    try:
        try:
            start_date = datetime.strptime(data['start_date'], '%m-%d-%Y').date()
            end_date = datetime.strptime(data['end_date'], '%m-%d-%Y').date()
        except ValueError:
            return jsonify({'error': 'Invalid date format. Use MM-DD-YYYY.'}), 400
        if start_date > end_date:
            return jsonify({'error': 'Start date cannot be after end date.'}), 400

        # Create a new itinerary
        new_itinerary = Itinerary(
            user_id=current_user.id,
            name=data['name'],
            start_date=start_date,
            end_date=end_date
        )
        db.session.add(new_itinerary)
        db.session.commit()

        activities_data = data.get('activities', [])
        for activity in activities_data:
            if not activity.get('name') or not activity.get('time'):
                continue
            new_activity = Activity(
                name=activity['name'],
                time=activity['time'],
                itinerary_id=new_itinerary.id
            )
            db.session.add(new_activity)

        db.session.commit()

        return jsonify(new_itinerary.to_dict()), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Update an itinerary
@itinerary_routes.route('/<int:id>', methods=['PUT'])
@login_required
def update_itinerary(id):
    data = request.json
    itinerary = Itinerary.query.get(id)

    if not itinerary or itinerary.user_id != current_user.id:
        return jsonify({'error': 'Itinerary not found or unauthorized'}), 404

    try:
        itinerary.name = data.get('name', itinerary.name)
        if 'start_date' in data:
            itinerary.start_date = datetime.strptime(data['start_date'], '%m-%d-%Y').date()
        if 'end_date' in data:
            itinerary.end_date = datetime.strptime(data['end_date'], '%m-%d-%Y').date()

        db.session.commit()
        return jsonify(itinerary.to_dict()), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Delete an itinerary
@itinerary_routes.route('/<int:id>', methods=['DELETE'])
@login_required
def delete_itinerary(id):
    itinerary = Itinerary.query.get(id)

    if not itinerary or itinerary.user_id != current_user.id:
        return jsonify({'error': 'Itinerary not found or unauthorized'}), 404

    try:
        db.session.delete(itinerary)
        db.session.commit()
        return jsonify({'message': 'Itinerary deleted successfully'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500