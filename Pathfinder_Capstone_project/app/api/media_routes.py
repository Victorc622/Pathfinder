from flask import Blueprint, jsonify, request, abort
from flask_login import login_required, current_user
from app.models import Media, Trip, db
import boto3
import os
from uuid import uuid4

media_routes = Blueprint('media', __name__)

s3 = boto3.client('s3', region_name=os.getenv('AWS_REGION'))


@media_routes.route('/<int:trip_id>', methods=['GET'])
@login_required
def get_media(trip_id):
    """
    Get all media files for a trip.
    """
    trip = Trip.query.get(trip_id)
    if not trip or trip.created_by != current_user.id:
        abort(404, description="Trip not found")

    media_files = Media.query.filter_by(trip_id=trip_id).all()
    return {'media': [media.to_dict() for media in media_files]}


@media_routes.route('/<int:trip_id>', methods=['POST'])
@login_required
def upload_media(trip_id):
    """
    Upload a media file for a trip.
    """
    trip = Trip.query.get(trip_id)
    if not trip or trip.created_by != current_user.id:
        abort(404, description="Trip not found")

    if 'file' not in request.files:
        abort(400, description="No file uploaded")

    file = request.files['file']
    filename = f"{uuid4()}_{file.filename}"

    try:
        s3.upload_fileobj(
            file,
            os.getenv('AWS_S3_BUCKET'),
            filename,
            ExtraArgs={'ACL': 'public-read'}
        )
        file_url = f"https://{os.getenv('AWS_S3_BUCKET')}.s3.amazonaws.com/{filename}"

        media = Media(
            trip_id=trip_id,
            file_url=file_url,
            uploaded_by=current_user.id
        )
        db.session.add(media)
        db.session.commit()

        return media.to_dict(), 201

    except Exception as e:
        abort(500, description=f"Failed to upload media: {str(e)}")


@media_routes.route('/<int:media_id>', methods=['DELETE'])
@login_required
def delete_media(media_id):
    """
    Delete a media file.
    """
    media = Media.query.get(media_id)
    if not media or media.trip.created_by != current_user.id:
        abort(404, description="Media not found")

    try:
        s3.delete_object(Bucket=os.getenv('AWS_S3_BUCKET'), Key=media.file_url.split('/')[-1])
    except Exception as e:
        print(f"Failed to delete media from S3: {str(e)}")

    db.session.delete(media)
    db.session.commit()
    return {'message': 'Media deleted successfully'}