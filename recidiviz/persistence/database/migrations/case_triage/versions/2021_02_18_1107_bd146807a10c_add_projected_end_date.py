# pylint: skip-file
"""add_projected_end_date

Revision ID: bd146807a10c
Revises: 41294530657a
Create Date: 2021-02-18 11:07:55.732327

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "bd146807a10c"
down_revision = "41294530657a"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "etl_clients", sa.Column("projected_end_date", sa.Date(), nullable=True)
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("etl_clients", "projected_end_date")
    # ### end Alembic commands ###
