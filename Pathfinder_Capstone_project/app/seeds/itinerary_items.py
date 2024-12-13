from app.models import db, ItineraryItem, environment, SCHEMA
from sqlalchemy.sql import text

def seed_itinerary_items():
    item1 = ItineraryItem(
        trip_id=1,
        user_id=1,
        title='Visit the beach',
        description='Spend the day relaxing on the sand.',
        start_time='2024-07-02 10:00:00',
        end_time='2024-07-02 17:00:00',
        location='Main Beach'
    )
    item2 = ItineraryItem(
        trip_id=2,
        user_id=2,
        title='Skiing at resort',
        description='Enjoy skiing all day.',
        start_time='2024-01-16 09:00:00',
        end_time='2024-01-16 16:00:00',
        location='Snowy Peaks Resort'
    )

    db.session.add(item1)
    db.session.add(item2)
    db.session.commit()

def undo_itinerary_items():
    if environment == "production":
        db.session.execute(f"TRUNCATE table {SCHEMA}.itinerary_items RESTART IDENTITY CASCADE;")
    else:
        db.session.execute(text("DELETE FROM itinerary_items"))
    db.session.commit()