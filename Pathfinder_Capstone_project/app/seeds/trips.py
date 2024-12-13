from app.models import db, Trip, environment, SCHEMA
from sqlalchemy.sql import text

def seed_trips():
    trip1 = Trip(
        title='Summer Vacation',
        description='A relaxing trip to the beach.',
        start_date='2024-07-01',
        end_date='2024-07-10',
        created_by=1,
        is_public=True
    )
    trip2 = Trip(
        title='Ski Adventure',
        description='A thrilling ski trip in the mountains.',
        start_date='2024-01-15',
        end_date='2024-01-20',
        created_by=2,
        is_public=False
    )

    db.session.add(trip1)
    db.session.add(trip2)
    db.session.commit()

def undo_trips():
    if environment == "production":
        db.session.execute(f"TRUNCATE table {SCHEMA}.trips RESTART IDENTITY CASCADE;")
    else:
        db.session.execute(text("DELETE FROM trips"))
    db.session.commit()