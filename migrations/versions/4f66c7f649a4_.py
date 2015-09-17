"""empty message

Revision ID: 4f66c7f649a4
Revises: 416925f7a48c
Create Date: 2015-09-17 09:39:13.372000

"""

# revision identifiers, used by Alembic.
revision = '4f66c7f649a4'
down_revision = '416925f7a48c'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key(None, 'demand_data', 'demand_profiles', ['demand_profile_id'], ['id'])
    op.create_foreign_key(None, 'demand_profiles', 'scenarios', ['scenario_id'], ['id'])
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'demand_profiles', type_='foreignkey')
    op.drop_constraint(None, 'demand_data', type_='foreignkey')
    ### end Alembic commands ###
