from .db import db, environment, SCHEMA, add_prefix_for_prod

class Activity(db.Model):
    __tablename__ = 'activities'

    if environment == "production":
        __table_args__ = {'schema': SCHEMA}

    id = db.Column(db.Integer, primary_key=True)
    destination_id = db.Column(
        db.Integer, 
        db.ForeignKey(add_prefix_for_prod('destinations.id')), 
        nullable=False
    )
    name = db.Column(db.String(255), nullable=False)
    time = db.Column(db.Time, nullable=False)

    destination = db.relationship(
        'Destination', 
        back_populates='activities'
    )

    def to_dict(self):
        return {
            'id': self.id,
            'destination_id': self.destination_id,
            'name': self.name,
            'time': str(self.time)
        }