from flask import Blueprint, request, jsonify
from app.models import Collaboration, Itinerary, User, db
from flask_login import current_user, login_required

collaboration_routes = Blueprint('collaborations', __name__)

# Add a collaborator to an itinerary
@collaboration_routes.route('/', methods=['POST'])
@login_required
def add_collaborator():
    data = request.json
    itinerary = Itinerary.query.get(data['itinerary_id'])
    if not itinerary or itinerary.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    user = User.query.filter_by(email=data['email']).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404
    new_collaboration = Collaboration(
        user_id=user.id,
        itinerary_id=itinerary.id
    )
    db.session.add(new_collaboration)
    db.session.commit()
    return jsonify(new_collaboration.to_dict())

# Remove a collaborator
@collaboration_routes.route('/<int:id>', methods=['DELETE'])
@login_required
def remove_collaborator(id):
    collaboration = Collaboration.query.get(id)
    if not collaboration or collaboration.itinerary.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    db.session.delete(collaboration)
    db.session.commit()
    return jsonify({'message': 'Collaborator removed successfully'})