from .db import db, environment, SCHEMA, add_prefix_for_prod
from datetime import datetime

class Trip(db.Model):
    __tablename__ = 'trips'

    if environment == "production":
        __table_args__ = {'schema': SCHEMA}

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    is_public = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    created_by_user = db.relationship('User', back_populates='trips')
    destinations = db.relationship('Destination', back_populates='trip', cascade='all, delete-orphan')
    itinerary_items = db.relationship('ItineraryItem', back_populates='trip', cascade='all, delete-orphan')
    collaborations = db.relationship('Collaboration', back_populates='trip', cascade='all, delete-orphan')
    media = db.relationship('Media', back_populates='trip', cascade='all, delete-orphan')
    comments = db.relationship('Comment', back_populates='trip', cascade='all, delete-orphan')

    def to_dict(self, include_relations=False):
        trip_dict = {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'start_date': self.start_date.isoformat(),
            'end_date': self.end_date.isoformat(),
            'created_by': self.created_by,
            'is_public': self.is_public,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
        }

        if include_relations:
            trip_dict['destinations'] = [dest.to_dict() for dest in self.destinations]
            trip_dict['itinerary_items'] = [item.to_dict() for item in self.itinerary_items]
            trip_dict['collaborations'] = [collab.to_dict() for collab in self.collaborations]
            trip_dict['media'] = [med.to_dict() for med in self.media]
            trip_dict['comments'] = [comm.to_dict() for comm in self.comments]

        return trip_dict

    def __repr__(self):
        return f"<Trip {self.title}>"