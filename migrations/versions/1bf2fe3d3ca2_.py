"""empty message

Revision ID: 1bf2fe3d3ca2
Revises: 37d0127f7699
Create Date: 2015-09-26 11:03:18.282000

"""

# revision identifiers, used by Alembic.
revision = '1bf2fe3d3ca2'
down_revision = '37d0127f7699'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('scenarios', sa.Column('forecast_horizon', sa.Integer(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('scenarios', 'forecast_horizon')
    ### end Alembic commands ###
