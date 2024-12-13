from app.models import db, Media, environment, SCHEMA
from sqlalchemy.sql import text

def seed_media():
    media1 = Media(
        trip_id=1,
        file_url='https://example.com/beach.jpg',
        uploaded_by=1
    )
    media2 = Media(
        trip_id=2,
        file_url='https://example.com/ski.jpg',
        uploaded_by=2
    )

    db.session.add(media1)
    db.session.add(media2)
    db.session.commit()

def undo_media():
    if environment == "production":
        db.session.execute(f"TRUNCATE table {SCHEMA}.media RESTART IDENTITY CASCADE;")
    else:
        db.session.execute(text("DELETE FROM media"))
    db.session.commit()