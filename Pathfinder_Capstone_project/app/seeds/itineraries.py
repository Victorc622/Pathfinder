from app.models import db, Itinerary, environment, SCHEMA
from sqlalchemy.sql import text

def seed_itineraries():
    itinerary1 = Itinerary(
        name='Summer Europe Trip',
        description='A two-week trip across Europe visiting key destinations.',
        user_id=1
    )
    itinerary2 = Itinerary(
        name='Winter Ski Adventure',
        description='Exploring the best ski resorts in the Alps.',
        user_id=2
    )
    itinerary3 = Itinerary(
        name='Beach Paradise',
        description='A tropical getaway to some of the world’s best beaches.',
        user_id=3
    )

    db.session.add(itinerary1)
    db.session.add(itinerary2)
    db.session.add(itinerary3)
    db.session.commit()

def undo_itineraries():
    if environment == "production":
        db.session.execute(f"TRUNCATE table {SCHEMA}.itineraries RESTART IDENTITY CASCADE;")
    else:
        db.session.execute(text("DELETE FROM itineraries"))
        
    db.session.commit()