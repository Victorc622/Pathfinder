from app.models import db, Destination, environment, SCHEMA
from sqlalchemy.sql import text

def seed_destinations():
    destination1 = Destination(name='Paris', country='France', description='City of lights and love.')
    destination2 = Destination(name='Tokyo', country='Japan', description='A bustling city blending modernity and tradition.')
    destination3 = Destination(name='Maui', country='USA', description='A tropical paradise with pristine beaches.')

    db.session.add(destination1)
    db.session.add(destination2)
    db.session.add(destination3)
    db.session.commit()

def undo_destinations():
    if environment == "production":
        db.session.execute(f"TRUNCATE table {SCHEMA}.destinations RESTART IDENTITY CASCADE;")
    else:
        db.session.execute(text("DELETE FROM destinations"))
        
    db.session.commit()