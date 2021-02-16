# pylint: skip-file
"""add_gender_and_supervision_start_date

Revision ID: 6f29ea64e99b
Revises: 239698677888
Create Date: 2021-02-11 10:31:00.917148

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6f29ea64e99b'
down_revision = '239698677888'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('etl_clients', sa.Column('gender', sa.String(length=255), nullable=True))
    op.add_column('etl_clients', sa.Column('supervision_start_date', sa.Date(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('etl_clients', 'supervision_start_date')
    op.drop_column('etl_clients', 'gender')
    # ### end Alembic commands ###