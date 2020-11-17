# pylint: skip-file
"""initial

Revision ID: 94280cd8cb93
Revises: 
Create Date: 2020-11-04 18:41:25.202836

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '94280cd8cb93'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('report_table_definition',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('system', sa.Enum('LAW_ENFORCEMENT', 'COURT_PROCESSES', 'CORRECTIONS', name='system'), nullable=True),
    sa.Column('metric_type', sa.Enum('ADMISSIONS', 'ARRESTS', 'POPULATION', 'REVOCATIONS', 'TERMINATIONS', name='metrictype'), nullable=True),
    sa.Column('measurement_type', sa.Enum('INSTANT', 'AVERAGE', 'DELTA', 'PERSON_BASED_DELTA', name='measurementtype'), nullable=True),
    sa.Column('filtered_dimensions', sa.ARRAY(sa.String(length=255)), nullable=True),
    sa.Column('filtered_dimension_values', sa.ARRAY(sa.String(length=255)), nullable=True),
    sa.Column('aggregated_dimensions', sa.ARRAY(sa.String(length=255)), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('metric_type', 'measurement_type', 'filtered_dimensions', 'filtered_dimension_values', 'aggregated_dimensions')
    )
    op.create_table('source',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('report',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('source_id', sa.Integer(), nullable=False),
    sa.Column('type', sa.String(length=255), nullable=False),
    sa.Column('instance', sa.String(length=255), nullable=False),
    sa.Column('publish_date', sa.Date(), nullable=False),
    sa.Column('acquisition_method', sa.Enum('SCRAPED', 'UPLOADED', 'MANUALLY_ENTERED', name='acquisitionmethod'), nullable=False),
    sa.ForeignKeyConstraint(['source_id'], ['source.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('source_id', 'type', 'instance')
    )
    op.create_table('report_table_instance',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('report_id', sa.Integer(), nullable=False),
    sa.Column('report_table_definition_id', sa.Integer(), nullable=False),
    sa.Column('time_window_start', sa.Date(), nullable=False),
    sa.Column('time_window_end', sa.Date(), nullable=False),
    sa.Column('methodology', sa.String(length=255), nullable=True),
    sa.ForeignKeyConstraint(['report_id'], ['report.id'], ),
    sa.ForeignKeyConstraint(['report_table_definition_id'], ['report_table_definition.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('report_id', 'report_table_definition_id', 'time_window_start', 'time_window_end')
    )
    op.create_table('cell',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('report_table_instance_id', sa.Integer(), nullable=False),
    sa.Column('aggregated_dimension_values', sa.ARRAY(sa.String(length=255)), nullable=False),
    sa.Column('value', sa.Numeric(), nullable=False),
    sa.ForeignKeyConstraint(['report_table_instance_id'], ['report_table_instance.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('report_table_instance_id', 'aggregated_dimension_values')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('cell')
    op.drop_table('report_table_instance')
    op.drop_table('report')
    op.drop_table('source')
    op.drop_table('report_table_definition')

    op.execute('DROP TYPE acquisitionmethod;')
    op.execute('DROP TYPE measurementtype;')
    op.execute('DROP TYPE metrictype;')
    op.execute('DROP TYPE system;')
    # ### end Alembic commands ###
