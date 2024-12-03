from app.models import db, Collaboration, environment, SCHEMA
from sqlalchemy.sql import text

def seed_collaborations():
    collaboration1 = Collaboration(
        user_id=1, itinerary_id=1, role='Editor'
    )
    collaboration2 = Collaboration(
        user_id=2, itinerary_id=2, role='Viewer'
    )
    collaboration3 = Collaboration(
        user_id=3, itinerary_id=3, role='Editor'
    )

    db.session.add(collaboration1)
    db.session.add(collaboration2)
    db.session.add(collaboration3)
    db.session.commit()

def undo_collaborations():
    if environment == "production":
        db.session.execute(f"TRUNCATE table {SCHEMA}.collaborations RESTART IDENTITY CASCADE;")
    else:
        db.session.execute(text("DELETE FROM collaborations"))
        
    db.session.commit()