from app.models import db, Destination, environment, SCHEMA
from sqlalchemy.sql import text

def seed_destinations():
    destination1 = Destination(
        trip_id=1,
        name='Miami Beach',
        latitude=25.790654,
        longitude=-80.1300455,
        notes='A popular tourist destination.'
    )
    destination2 = Destination(
        trip_id=2,
        name='Aspen Mountain',
        latitude=39.1911,
        longitude=-106.8175,
        notes='Known for its ski resorts.'
    )

    db.session.add(destination1)
    db.session.add(destination2)
    db.session.commit()

def undo_destinations():
    if environment == "production":
        db.session.execute(f"TRUNCATE table {SCHEMA}.destinations RESTART IDENTITY CASCADE;")
    else:
        db.session.execute(text("DELETE FROM destinations"))
    db.session.commit()