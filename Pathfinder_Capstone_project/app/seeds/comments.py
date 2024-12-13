from app.models import db, Comment, environment, SCHEMA
from sqlalchemy.sql import text

def seed_comments():
    comment1 = Comment(
        trip_id=1,
        user_id=2,
        content='This trip looks amazing!'
    )
    comment2 = Comment(
        trip_id=2,
        user_id=1,
        content='Can’t wait to join this trip!'
    )

    db.session.add(comment1)
    db.session.add(comment2)
    db.session.commit()

def undo_comments():
    if environment == "production":
        db.session.execute(f"TRUNCATE table {SCHEMA}.comments RESTART IDENTITY CASCADE;")
    else:
        db.session.execute(text("DELETE FROM comments"))
    db.session.commit()