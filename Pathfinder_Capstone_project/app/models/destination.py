from .db import db, environment, SCHEMA, add_prefix_for_prod

class Destination(db.Model):
    __tablename__ = 'destinations'

    if environment == "production":
        __table_args__ = {'schema': SCHEMA}

    id = db.Column(db.Integer, primary_key=True)
    itinerary_id = db.Column(db.Integer, db.ForeignKey(add_prefix_for_prod('itineraries.id')), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(500), nullable=True)

    itinerary = db.relationship('Itinerary', back_populates='destinations')
    activities = db.relationship('Activity', back_populates='destination', cascade="all, delete-orphan")

    def to_dict(self):
        return {
            'id': self.id,
            'itinerary_id': self.itinerary_id,
            'name': self.name,
            'description': self.description
        }