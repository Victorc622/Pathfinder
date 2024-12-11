from flask import Blueprint, jsonify, request, abort
from flask_login import login_required, current_user
from app.models import Comment, Trip, db

comment_routes = Blueprint('comments', __name__)

@comment_routes.route('/<int:trip_id>', methods=['GET'])
@login_required
def get_comments(trip_id):
    """
    Get all comments for a trip.
    """
    trip = Trip.query.get(trip_id)
    if not trip:
        abort(404, description="Trip not found")

    comments = Comment.query.filter_by(trip_id=trip_id).all()
    return {'comments': [comment.to_dict() for comment in comments]}


@comment_routes.route('/<int:trip_id>', methods=['POST'])
@login_required
def add_comment(trip_id):
    """
    Add a comment to a trip.
    """
    trip = Trip.query.get(trip_id)
    if not trip:
        abort(404, description="Trip not found")

    data = request.get_json()
    comment = Comment(
        trip_id=trip_id,
        user_id=current_user.id,
        content=data['content']
    )
    db.session.add(comment)
    db.session.commit()
    return comment.to_dict(), 201


@comment_routes.route('/<int:comment_id>', methods=['PUT'])
@login_required
def update_comment(comment_id):
    """
    Edit a comment.
    """
    comment = Comment.query.get(comment_id)
    if not comment or comment.user_id != current_user.id:
        abort(404, description="Comment not found")

    data = request.get_json()
    comment.content = data.get('content', comment.content)

    db.session.commit()
    return comment.to_dict()


@comment_routes.route('/<int:comment_id>', methods=['DELETE'])
@login_required
def delete_comment(comment_id):
    """
    Delete a comment.
    """
    comment = Comment.query.get(comment_id)
    if not comment or comment.user_id != current_user.id:
        abort(404, description="Comment not found")

    db.session.delete(comment)
    db.session.commit()
    return {'message': 'Comment deleted successfully'}