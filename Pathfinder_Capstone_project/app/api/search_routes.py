from flask import Blueprint, request, jsonify
from app.models import Destination, Itinerary, db
from flask_login import login_required, current_user

search_routes = Blueprint('search', __name__)

# Search destinations by name
@search_routes.route('/destinations', methods=['GET'])
@login_required
def search_destinations():
    search_query = request.args.get('query', '')
    if not search_query:
        return jsonify({'error': 'Search query is required'}), 400

    destinations = Destination.query.filter(Destination.name.ilike(f'%{search_query}%')).all()
    return jsonify([destination.to_dict() for destination in destinations])

# Search itineraries by name
@search_routes.route('/itineraries', methods=['GET'])
@login_required
def search_itineraries():
    search_query = request.args.get('query', '')
    if not search_query:
        return jsonify({'error': 'Search query is required'}), 400

    itineraries = Itinerary.query.filter(Itinerary.name.ilike(f'%{search_query}%')).filter_by(user_id=current_user.id).all()
    return jsonify([itinerary.to_dict() for itinerary in itineraries])
