from .db import db, environment, SCHEMA, add_prefix_for_prod

class Itinerary(db.Model):
    __tablename__ = 'itineraries'

    if environment == "production":
        __table_args__ = {'schema': SCHEMA}

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(add_prefix_for_prod('users.id')), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)

    user = db.relationship('User', back_populates='itineraries')
    destinations = db.relationship('Destination', back_populates='itinerary', cascade="all, delete-orphan")
    collaborations = db.relationship('Collaboration', back_populates='itinerary')

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'start_date': str(self.start_date),
            'end_date': str(self.end_date)
        }