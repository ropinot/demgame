"""empty message

Revision ID: 46faa518903b
Revises: 456c181a7a96
Create Date: 2015-09-27 22:59:49.427000

"""

# revision identifiers, used by Alembic.
revision = '46faa518903b'
down_revision = '456c181a7a96'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('scenarios', sa.Column('frozen_horizon', sa.Integer(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('scenarios', 'frozen_horizon')
    ### end Alembic commands ###
