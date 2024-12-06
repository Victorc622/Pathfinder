from flask import Blueprint, request, session, jsonify
from app.models import User, db
from app.forms import LoginForm, SignUpForm
from flask_login import current_user, login_user, logout_user, login_required

auth_routes = Blueprint('auth', __name__)

@auth_routes.route('/')
def authenticate():
    """
    Authenticates a user.
    """
    if current_user.is_authenticated:
        return current_user.to_dict()
    return {'errors': {'message': 'Unauthorized'}}, 401

@auth_routes.route('/login', methods=['POST'])
def login():
    """
    Logs a user in
    """
    form = LoginForm()
    form['csrf_token'].data = request.cookies['csrf_token']

    if form.validate_on_submit():
        user = User.query.filter(User.email == form.data['email']).first()
        if user and user.check_password(form.data['password']):
            login_user(user)
            return user.to_dict()
        elif user:
            return jsonify({'errors': {'password': ['Incorrect password.']}}), 401
        else:
            return jsonify({'errors': {'email': ['Email not found.']}}), 401

    return jsonify({'errors': form.errors}), 401

@auth_routes.route('/logout', methods=['POST'])
def logout():
    logout_user()
    session.clear()
    session.permanent = False
    return {'message': 'User logged out'}

@auth_routes.route('/signup', methods=['POST'])
def sign_up():
    """
    Creates a new user and logs them in, with feedback for duplicate credentials
    """
    form = SignUpForm()
    form['csrf_token'].data = request.cookies['csrf_token']

    if User.query.filter_by(email=form.data['email']).first():
        return jsonify({'errors': {'email': 'Email is already in use'}}), 400

    if User.query.filter_by(username=form.data['username']).first():
        return jsonify({'errors': {'username': ['Username is already in use.']}}), 400

    if form.validate_on_submit():
        try:
            user = User(
                username=form.data['username'],
                email=form.data['email'],
                password=form.data['password']
            )
            db.session.add(user)
            db.session.commit()
            login_user(user)
            return user.to_dict()
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': f'Failed to create user: {str(e)}'}), 500

    return jsonify({'errors': form.errors}), 401

@auth_routes.route('/unauthorized')
def unauthorized():
    """
    Returns unauthorized JSON when flask-login authentication fails
    """
    return {'errors': {'message': 'Unauthorized'}}, 401