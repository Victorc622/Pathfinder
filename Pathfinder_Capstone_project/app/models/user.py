from .db import db, environment, SCHEMA, add_prefix_for_prod
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    if environment == "production":
        __table_args__ = {'schema': SCHEMA}

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), nullable=False, unique=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    hashed_password = db.Column(db.String(255), nullable=False)

    itineraries = db.relationship('Itinerary', back_populates='user')
    collaborations = db.relationship('Collaboration', back_populates='user')

    @property
    def password(self):
        return self.hashed_password

    @password.setter
    def password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def to_dict(self, include_relations=False):
        user_dict = {
            'id': self.id,
            'username': self.username,
            'email': self.email
        }
        if include_relations:
            user_dict['itineraries'] = [itinerary.to_dict() for itinerary in self.itineraries]
            user_dict['collaborations'] = [collab.to_dict() for collab in self.collaborations]
        return user_dict