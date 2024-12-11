from flask import Blueprint, jsonify, request, abort
from flask_login import login_required, current_user
from app.models import Collaboration, Trip, User, db

collaboration_routes = Blueprint('collaborations', __name__)

@collaboration_routes.route('/<int:trip_id>', methods=['GET'])
@login_required
def get_collaborators(trip_id):
    """
    Get all collaborators for a trip.
    """
    trip = Trip.query.get(trip_id)
    if not trip or trip.created_by != current_user.id:
        abort(404, description="Trip not found")

    collaborators = Collaboration.query.filter_by(trip_id=trip_id).all()
    return {'collaborators': [collab.to_dict() for collab in collaborators]}


@collaboration_routes.route('/<int:trip_id>', methods=['POST'])
@login_required
def add_collaborator(trip_id):
    """
    Add a collaborator to a trip.
    """
    trip = Trip.query.get(trip_id)
    if not trip or trip.created_by != current_user.id:
        abort(404, description="Trip not found")

    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    if not user:
        abort(404, description="User not found")

    collaboration = Collaboration(
        trip_id=trip_id,
        user_id=user.id,
        role=data.get('role', 'viewer')
    )
    db.session.add(collaboration)
    db.session.commit()
    return collaboration.to_dict(), 201


@collaboration_routes.route('/<int:collab_id>', methods=['PUT'])
@login_required
def update_collaborator(collab_id):
    """
    Update a collaborator's role.
    """
    collaboration = Collaboration.query.get(collab_id)
    if not collaboration or collaboration.trip.created_by != current_user.id:
        abort(404, description="Collaboration not found")

    data = request.get_json()
    collaboration.role = data.get('role', collaboration.role)

    db.session.commit()
    return collaboration.to_dict()


@collaboration_routes.route('/<int:collab_id>', methods=['DELETE'])
@login_required
def remove_collaborator(collab_id):
    """
    Remove a collaborator from a trip.
    """
    collaboration = Collaboration.query.get(collab_id)
    if not collaboration or collaboration.trip.created_by != current_user.id:
        abort(404, description="Collaboration not found")

    db.session.delete(collaboration)
    db.session.commit()
    return {'message': 'Collaborator removed successfully'}
