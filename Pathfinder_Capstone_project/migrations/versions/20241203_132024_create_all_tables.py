"""Create all tables

Revision ID: bbf7230257d1
Revises: 
Create Date: 2024-12-03 13:20:24.716617

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bbf7230257d1'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=40), nullable=False),
    sa.Column('email', sa.String(length=255), nullable=False),
    sa.Column('hashed_password', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('itineraries',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('start_date', sa.Date(), nullable=False),
    sa.Column('end_date', sa.Date(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('collaborations',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('itinerary_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['itinerary_id'], ['itineraries.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('destinations',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('itinerary_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('description', sa.String(length=500), nullable=True),
    sa.ForeignKeyConstraint(['itinerary_id'], ['itineraries.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('activities',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('destination_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('time', sa.Time(), nullable=False),
    sa.ForeignKeyConstraint(['destination_id'], ['destinations.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('activities')
    op.drop_table('destinations')
    op.drop_table('collaborations')
    op.drop_table('itineraries')
    op.drop_table('users')
    # ### end Alembic commands ###