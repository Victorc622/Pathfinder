from flask import Blueprint, request, session, jsonify, abort
from app.models import User, db
from app.forms import LoginForm, SignUpForm
from flask_login import current_user, login_user, logout_user, login_required

auth_routes = Blueprint('auth', __name__)


@auth_routes.route('/')
def authenticate():
    """
    Check if the user is authenticated and return their profile.
    """
    if current_user.is_authenticated:
        return current_user.to_dict(include_relations=True)
    return {'errors': {'message': 'Unauthorized'}}, 401


@auth_routes.route('/login', methods=['POST'])
def login():
    """
    Log a user in.
    """
    form = LoginForm()
    form['csrf_token'].data = request.cookies['csrf_token']

    if form.validate_on_submit():
        user = User.query.filter(User.email == form.data['email']).first()
        if user and user.check_password(form.data['password']):
            login_user(user)
            return user.to_dict(include_relations=True)
        return jsonify({'errors': {'message': 'Invalid email or password'}}), 401

    return jsonify({'errors': form.errors}), 401


@auth_routes.route('/logout', methods=['POST'])
def logout():
    """
    Log the current user out and clear their session.
    """
    logout_user()
    session.clear()
    return {'message': 'User logged out'}


@auth_routes.route('/signup', methods=['POST'])
def sign_up():
    """
    Create a new user and log them in, with validation for duplicates.
    """
    form = SignUpForm()
    form['csrf_token'].data = request.cookies['csrf_token']

    # Validate email and username uniqueness
    if User.query.filter_by(email=form.data['email']).first():
        return jsonify({'errors': {'email': ['Email already in use']}}), 409

    if User.query.filter_by(username=form.data['username']).first():
        return jsonify({'errors': {'username': ['Username already in use']}}), 409

    if form.validate_on_submit():
        try:
            user = User(
                username=form.data['username'],
                email=form.data['email'],
                password=form.data['password']  # Uses setter to hash password
            )
            db.session.add(user)
            db.session.commit()
            login_user(user)
            return user.to_dict(include_relations=True)
        except Exception as e:
            db.session.rollback()
            return jsonify({'errors': {'message': f'Failed to create user: {str(e)}'}}), 500

    return jsonify({'errors': form.errors}), 401


@auth_routes.route('/unauthorized')
def unauthorized():
    """
    Return a JSON response when flask-login authentication fails.
    """
    return {'errors': {'message': 'Unauthorized'}}, 401


@auth_routes.route('/update-password', methods=['POST'])
@login_required
def update_password():
    """
    Allow a logged-in user to update their password.
    """
    data = request.get_json()
    old_password = data.get('old_password')
    new_password = data.get('new_password')

    if not current_user.check_password(old_password):
        return jsonify({'errors': {'password': ['Incorrect current password']}}), 401

    current_user.password = new_password
    db.session.commit()
    return {'message': 'Password updated successfully'}