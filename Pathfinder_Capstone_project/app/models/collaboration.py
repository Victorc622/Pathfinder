from .db import db, environment, SCHEMA, add_prefix_for_prod
from datetime import datetime

class Collaboration(db.Model):
    __tablename__ = 'collaborations'

    if environment == "production":
        __table_args__ = {'schema': SCHEMA}

    id = db.Column(db.Integer, primary_key=True)
    trip_id = db.Column(db.Integer, db.ForeignKey('trips.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    role = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    trip = db.relationship('Trip', back_populates='collaborations')
    user = db.relationship('User', back_populates='collaborations')

    def to_dict(self):
        return {
            'id': self.id,
            'trip_id': self.trip_id,
            'user_id': self.user_id,
            'role': self.role,
            'created_at': self.created_at.isoformat(),
        }

    def __repr__(self):
        return f"<Collaboration Trip: {self.trip_id}, User: {self.user_id}, Role: {self.role}>"