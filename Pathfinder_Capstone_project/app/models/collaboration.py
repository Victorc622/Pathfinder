from .db import db, environment, SCHEMA, add_prefix_for_prod

class Collaboration(db.Model):
    __tablename__ = 'collaborations'

    if environment == "production":
        __table_args__ = {'schema': SCHEMA}

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(add_prefix_for_prod('users.id')), nullable=False)
    itinerary_id = db.Column(db.Integer, db.ForeignKey(add_prefix_for_prod('itineraries.id')), nullable=False)

    user = db.relationship('User', back_populates='collaborations')
    itinerary = db.relationship('Itinerary', back_populates='collaborations')

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'itinerary_id': self.itinerary_id
        }