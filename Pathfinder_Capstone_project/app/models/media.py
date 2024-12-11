from .db import db, environment, SCHEMA, add_prefix_for_prod
from datetime import datetime

class Media(db.Model):
    __tablename__ = 'media'

    if environment == "production":
        __table_args__ = {'schema': SCHEMA}

    id = db.Column(db.Integer, primary_key=True)
    trip_id = db.Column(db.Integer, db.ForeignKey('trips.id'), nullable=False)
    file_url = db.Column(db.String(255), nullable=False)
    uploaded_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)

    trip = db.relationship('Trip', back_populates='media')
    uploader = db.relationship('User', back_populates='media')

    def to_dict(self):
        return {
            'id': self.id,
            'trip_id': self.trip_id,
            'file_url': self.file_url,
            'uploaded_by': self.uploaded_by,
            'uploaded_at': self.uploaded_at.isoformat(),
        }

    def __repr__(self):
        return f"<Media Trip: {self.trip_id}, Uploaded By: {self.uploaded_by}>"