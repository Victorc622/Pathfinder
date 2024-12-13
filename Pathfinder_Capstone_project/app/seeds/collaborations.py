from app.models import db, Collaboration, environment, SCHEMA
from sqlalchemy.sql import text

def seed_collaborations():
    collab1 = Collaboration(
        trip_id=1,
        user_id=2,
        role='editor'
    )
    collab2 = Collaboration(
        trip_id=2,
        user_id=1,
        role='viewer'
    )

    db.session.add(collab1)
    db.session.add(collab2)
    db.session.commit()

def undo_collaborations():
    if environment == "production":
        db.session.execute(f"TRUNCATE table {SCHEMA}.collaborations RESTART IDENTITY CASCADE;")
    else:
        db.session.execute(text("DELETE FROM collaborations"))
    db.session.commit()