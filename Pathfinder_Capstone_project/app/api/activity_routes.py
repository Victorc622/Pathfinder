from flask import Blueprint, request, jsonify
from app.models import db
from flask_login import login_required, current_user

activities_routes = Blueprint('activities', __name__)

# Create a new activity
@activities_routes.route('/activities', methods=['POST'])
@login_required
def create_activity():
    from app.models import Activity
    data = request.get_json()
    
    name = data.get('name')
    description = data.get('description')
    destination_id = data.get('destination_id')
    itinerary_id = data.get('itinerary_id')
    
    if not name or not description or not destination_id:
        return jsonify({'error': 'Missing required fields'}), 400

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

# View all activities (either by destination or itinerary)
@activities_routes.route('/activities', methods=['GET'])
@login_required
def get_activities():
    from app.models import Activity  # Import Activity here to avoid circular import
    itinerary_id = request.args.get('itinerary_id')
    destination_id = request.args.get('destination_id')

    if itinerary_id:
        activities = Activity.query.filter_by(itinerary_id=itinerary_id).all()
    elif destination_id:
        activities = Activity.query.filter_by(destination_id=destination_id).all()
    else:
        return jsonify({'error': 'Must provide either itinerary_id or destination_id'}), 400
    
    return jsonify([activity.to_dict() for activity in activities])

# Update an existing activity
@activities_routes.route('/activities/<int:activity_id>', methods=['PUT'])
@login_required
def update_activity(activity_id):
    from app.models import Activity  # Import Activity here to avoid circular import
    data = request.get_json()
    
    activity = Activity.query.get_or_404(activity_id)

    # Ensure the activity belongs to the logged-in user
    if activity.itinerary.user_id != current_user.id:
        return jsonify({'error': 'Not authorized to edit this activity'}), 403

    name = data.get('name', activity.name)
    description = data.get('description', activity.description)

    activity.name = name
    activity.description = description

    db.session.commit()

    return jsonify(activity.to_dict())

# Delete an existing activity
@activities_routes.route('/activities/<int:activity_id>', methods=['DELETE'])
@login_required
def delete_activity(activity_id):
    from app.models import Activity  # Import Activity here to avoid circular import
    activity = Activity.query.get_or_404(activity_id)

    # Ensure the activity belongs to the logged-in user
    if activity.itinerary.user_id != current_user.id:
        return jsonify({'error': 'Not authorized to delete this activity'}), 403

    db.session.delete(activity)
    db.session.commit()

    return jsonify({'message': 'Activity deleted successfully'}), 200