# pylint: skip-file
"""add_employment

Revision ID: d75894b38f4f
Revises: 644f6fd3fec1
Create Date: 2021-01-25 08:34:26.064516

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd75894b38f4f'
down_revision = '644f6fd3fec1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('etl_clients', sa.Column('employer', sa.String(length=255), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('etl_clients', 'employer')
    # ### end Alembic commands ###