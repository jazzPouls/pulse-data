"""tn_aggregate

Revision ID: efb33d3b6772
Revises: 16f89aa16e0e
Create Date: 2019-03-13 11:16:53.444191

"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = 'efb33d3b6772'
down_revision = '16f89aa16e0e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tn_facility_female_aggregate',
    sa.Column('record_id', sa.Integer(), nullable=False),
    sa.Column('fips', sa.String(length=255), nullable=False),
    sa.Column('report_date', sa.Date(), nullable=False),
    sa.Column('report_granularity', postgresql.ENUM('DAILY', 'WEEKLY', 'MONTHLY', 'QUARTERLY', 'YEARLY', create_type=False, name='report_granularity'), nullable=False),
    sa.Column('facility_name', sa.Integer(), nullable=True),
    sa.Column('tdoc_backup_population', sa.Integer(), nullable=True),
    sa.Column('local_felons_population', sa.Integer(), nullable=True),
    sa.Column('other_convicted_felons_population', sa.Integer(), nullable=True),
    sa.Column('federal_and_other_population', sa.Integer(), nullable=True),
    sa.Column('convicted_misdemeanor_population', sa.Integer(), nullable=True),
    sa.Column('pretrial_felony_population', sa.Integer(), nullable=True),
    sa.Column('pretrial_misdemeanor_population', sa.Integer(), nullable=True),
    sa.Column('female_jail_population', sa.Integer(), nullable=True),
    sa.Column('female_beds', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('record_id'),
    sa.UniqueConstraint('fips', 'facility_name', 'report_date', 'report_granularity')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('tn_facility_female_aggregate')
    # ### end Alembic commands ###