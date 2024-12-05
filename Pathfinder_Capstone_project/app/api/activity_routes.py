from flask import Blueprint, request, jsonify
from app.models import db, Activity, Itinerary
from flask_login import login_required, current_user

activities_routes = Blueprint('activities', __name__)

# Create a new activity
@activities_routes.route('/', methods=['POST'])
@login_required
def create_activity():
    """
    Creates a new activity for a given itinerary or destination.
    """
    data = request.get_json()
    
    name = data.get('name')
    description = data.get('description')
    destination_id = data.get('destination_id')
    itinerary_id = data.get('itinerary_id')
    
    if not name or not description or not destination_id or not itinerary_id:
        return jsonify({'error': 'Missing required fields: name, description, destination_id, or itinerary_id'}), 400

    itinerary = Itinerary.query.get(itinerary_id)
    if not itinerary or itinerary.user_id != current_user.id:
        return jsonify({'error': 'Not authorized to add activities to this itinerary'}), 403

    # Create the new activity
    activity = Activity(
        name=name,
        description=description,
        destination_id=destination_id,
        itinerary_id=itinerary_id
    )

    db.session.add(activity)
    db.session.commit()

    return jsonify(activity.to_dict()), 201

# View all activities (filtered by itinerary or destination)
@activities_routes.route('/', methods=['GET'])
@login_required
def get_activities():
    """
    Retrieves all activities filtered by itinerary or destination.
    """
    itinerary_id = request.args.get('itinerary_id')
    destination_id = request.args.get('destination_id')

    if not itinerary_id and not destination_id:
        return jsonify({'error': 'Must provide either itinerary_id or destination_id'}), 400

    if itinerary_id:
        itinerary = Itinerary.query.get(itinerary_id)
        if not itinerary or itinerary.user_id != current_user.id:
            return jsonify({'error': 'Not authorized to view activities for this itinerary'}), 403
        activities = Activity.query.filter_by(itinerary_id=itinerary_id).all()
    elif destination_id:
        activities = Activity.query.filter_by(destination_id=destination_id).all()

    return jsonify([activity.to_dict() for activity in activities]), 200

# Update an existing activity
@activities_routes.route('/<int:activity_id>', methods=['PUT'])
@login_required
def update_activity(activity_id):
    """
    Updates an existing activity.
    """
    data = request.get_json()
    
    activity = Activity.query.get(activity_id)
    if not activity:
        return jsonify({'error': 'Activity not found'}), 404

    if activity.itinerary.user_id != current_user.id:
        return jsonify({'error': 'Not authorized to edit this activity'}), 403

    activity.name = data.get('name', activity.name)
    activity.description = data.get('description', activity.description)

    db.session.commit()

    return jsonify(activity.to_dict()), 200

# Delete an existing activity
@activities_routes.route('/<int:activity_id>', methods=['DELETE'])
@login_required
def delete_activity(activity_id):
    """
    Deletes an activity.
    """
    activity = Activity.query.get(activity_id)
    if not activity:
        return jsonify({'error': 'Activity not found'}), 404

    if activity.itinerary.user_id != current_user.id:
        return jsonify({'error': 'Not authorized to delete this activity'}), 403

    db.session.delete(activity)
    db.session.commit()

    return jsonify({'message': 'Activity deleted successfully'}), 200