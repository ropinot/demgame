"""empty message

Revision ID: 3102de9f9b2c
Revises: 2b99504ab12b
Create Date: 2015-09-15 19:27:31.292000

"""

# revision identifiers, used by Alembic.
revision = '3102de9f9b2c'
down_revision = '2b99504ab12b'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('scenarios',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.Column('duration', sa.Integer(), nullable=True),
    sa.Column('leadtime', sa.Integer(), nullable=True),
    sa.Column('product_cost', sa.Float(), nullable=True),
    sa.Column('stock_cost', sa.Float(), nullable=True),
    sa.Column('lostsale_cost', sa.Float(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('scenarios')
    ### end Alembic commands ###