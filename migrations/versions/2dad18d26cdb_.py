"""empty message

Revision ID: 2dad18d26cdb
Revises: 561323c9fdab
Create Date: 2015-09-16 17:22:43.256000

"""

# revision identifiers, used by Alembic.
revision = '2dad18d26cdb'
down_revision = '561323c9fdab'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('gameboards', sa.Column('data', sa.PickleType(), nullable=True))
    op.drop_column('gameboards', 'tablestring')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('gameboards', sa.Column('tablestring', postgresql.BYTEA(), autoincrement=False, nullable=True))
    op.drop_column('gameboards', 'data')
    ### end Alembic commands ###
