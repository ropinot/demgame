"""empty message

Revision ID: 2406e56992ca
Revises: 3102de9f9b2c
Create Date: 2015-09-15 22:07:37.994000

"""

# revision identifiers, used by Alembic.
revision = '2406e56992ca'
down_revision = '3102de9f9b2c'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('players',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('login', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('scenario_counters',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('player_id', sa.Integer(), nullable=True),
    sa.Column('scenario_id', sa.Integer(), nullable=True),
    sa.Column('current', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['player_id'], ['players.id'], ),
    sa.ForeignKeyConstraint(['scenario_id'], ['scenarios.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column(u'decisions', sa.Column('player_id', sa.Integer(), nullable=True))
    op.add_column(u'decisions', sa.Column('scenario_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'decisions', 'players', ['player_id'], ['id'])
    op.create_foreign_key(None, 'decisions', 'scenarios', ['scenario_id'], ['id'])
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'decisions', type_='foreignkey')
    op.drop_constraint(None, 'decisions', type_='foreignkey')
    op.drop_column(u'decisions', 'scenario_id')
    op.drop_column(u'decisions', 'player_id')
    op.drop_table('scenario_counters')
    op.drop_table('players')
    ### end Alembic commands ###
