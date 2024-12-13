from flask.cli import AppGroup
from .users import seed_users, undo_users
from .trips import seed_trips, undo_trips
from .itinerary_items import seed_itinerary_items, undo_itinerary_items
from .destinations import seed_destinations, undo_destinations
from .collaborations import seed_collaborations, undo_collaborations
from .comments import seed_comments, undo_comments
from .media import seed_media, undo_media

from app.models.db import db, environment, SCHEMA

# Creates a seed group to hold our commands
# So we can type `flask seed --help`
seed_commands = AppGroup('seed')


# Creates the `flask seed all` command
@seed_commands.command('all')
def seed():
    """
    Seed all tables in the correct order.
    """
    if environment == 'production':
        # Before seeding in production, you want to run the seed undo 
        # command to clear tables prefixed with the schema name.
        undo_users()
        undo_trips()
        undo_itinerary_items()
        undo_destinations()
        undo_collaborations()
        undo_comments()
        undo_media()

    # Seed all models in the correct order
    seed_users()
    seed_trips()
    seed_itinerary_items()
    seed_destinations()
    seed_collaborations()
    seed_comments()
    seed_media()


# Creates the `flask seed undo` command
@seed_commands.command('undo')
def undo():
    """
    Undo all seeds in the correct order.
    """
    undo_media()
    undo_comments()
    undo_collaborations()
    undo_destinations()
    undo_itinerary_items()
    undo_trips()
    undo_users()