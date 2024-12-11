from .db import db, environment, SCHEMA, add_prefix_for_prod
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    if environment == "production":
        __table_args__ = {'schema': SCHEMA}

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), nullable=False, unique=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    hashed_password = db.Column(db.String(255), nullable=False)
    profile_picture = db.Column(db.String(255), nullable=True)  # URL for profile picture
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    trips = db.relationship('Trip', back_populates='created_by_user', cascade='all, delete-orphan')
    itinerary_items = db.relationship('ItineraryItem', back_populates='user', cascade='all, delete-orphan')
    collaborations = db.relationship('Collaboration', back_populates='user', cascade='all, delete-orphan')
    media = db.relationship('Media', back_populates='uploader', cascade='all, delete-orphan')
    comments = db.relationship('Comment', back_populates='user', cascade='all, delete-orphan')

    # Password handling
    @property
    def password(self):
        return self.hashed_password

    @password.setter
    def password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)

    # Convert user object to dictionary
    def to_dict(self, include_relations=False):
        user_dict = {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'profile_picture': self.profile_picture,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

        if include_relations:
            user_dict['trips'] = [trip.to_dict() for trip in self.trips]
            user_dict['itinerary_items'] = [item.to_dict() for item in self.itinerary_items]
            user_dict['collaborations'] = [collaboration.to_dict() for collaboration in self.collaborations]

        return user_dict

    def __repr__(self):
        return f"<User {self.username}>"