from flask import Blueprint, jsonify, request, abort
from flask_login import login_required, current_user
from app.models import User, Trip, Collaboration

user_routes = Blueprint('users', __name__)

@user_routes.route('/')
@login_required
def users():
    """
    Query for all users and return them in a list of user dictionaries.
    """
    users = User.query.all()
    return {'users': [user.to_dict() for user in users]}


@user_routes.route('/<int:id>')
@login_required
def user(id):
    """
    Query for a user by ID and return their data in a dictionary.
    """
    user = User.query.get(id)
    if not user:
        abort(404, description="User not found")
    return user.to_dict(include_relations=True)


@user_routes.route('/<int:id>/trips')
@login_required
def user_trips(id):
    """
    Query for all trips created by a user and return them in a list of trip dictionaries.
    """
    user = User.query.get(id)
    if not user:
        abort(404, description="User not found")
    trips = Trip.query.filter_by(created_by=id).all()
    return {'trips': [trip.to_dict() for trip in trips]}


@user_routes.route('/<int:id>/collaborations')
@login_required
def user_collaborations(id):
    """
    Query for all trips a user is collaborating on and return them in a list of collaboration dictionaries.
    """
    collaborations = Collaboration.query.filter_by(user_id=id).all()
    return {'collaborations': [collab.to_dict() for collab in collaborations]}


@user_routes.route('/profile')
@login_required
def profile():
    """
    Get the profile of the currently logged-in user, including their trips and collaborations.
    """
    return current_user.to_dict(include_relations=True)