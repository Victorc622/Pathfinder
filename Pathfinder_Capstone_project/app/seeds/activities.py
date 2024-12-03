from app.models import db, Activity, environment, SCHEMA
from sqlalchemy.sql import text

def seed_activities():
    activity1 = Activity(
        name='Eiffel Tower Visit', description='Tour and view from the Eiffel Tower', itinerary_id=1
    )
    activity2 = Activity(
        name='Shibuya Crossing Walk', description='Experience the famous Tokyo crossing.', itinerary_id=2
    )
    activity3 = Activity(
        name='Snorkeling in Maui', description='Explore underwater beauty in Maui.', itinerary_id=3
    )

    db.session.add(activity1)
    db.session.add(activity2)
    db.session.add(activity3)
    db.session.commit()

def undo_activities():
    if environment == "production":
        db.session.execute(f"TRUNCATE table {SCHEMA}.activities RESTART IDENTITY CASCADE;")
    else:
        db.session.execute(text("DELETE FROM activities"))
        
    db.session.commit()