"""add_incarceration_purpose

Revision ID: b32740e287af
Revises: fac36567b24b
Create Date: 2019-12-06 12:59:04.095045

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
from sqlalchemy.dialects import postgresql

revision = "b32740e287af"
down_revision = "fac36567b24b"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    specialized_purpose_for_incarceration = postgresql.ENUM(
        "SHOCK_INCARCERATION",
        "TREATMENT_IN_PRISON",
        name="state_specialized_purpose_for_incarceration",
    )
    specialized_purpose_for_incarceration.create(op.get_bind())
    op.add_column(
        "state_incarceration_period",
        sa.Column(
            "specialized_purpose_for_incarceration",
            sa.Enum(
                "SHOCK_INCARCERATION",
                "TREATMENT_IN_PRISON",
                name="state_specialized_purpose_for_incarceration",
            ),
            nullable=True,
        ),
    )
    op.add_column(
        "state_incarceration_period",
        sa.Column(
            "specialized_purpose_for_incarceration_raw_text",
            sa.String(length=255),
            nullable=True,
        ),
    )
    op.add_column(
        "state_incarceration_period_history",
        sa.Column(
            "specialized_purpose_for_incarceration",
            sa.Enum(
                "SHOCK_INCARCERATION",
                "TREATMENT_IN_PRISON",
                name="state_specialized_purpose_for_incarceration",
            ),
            nullable=True,
        ),
    )
    op.add_column(
        "state_incarceration_period_history",
        sa.Column(
            "specialized_purpose_for_incarceration_raw_text",
            sa.String(length=255),
            nullable=True,
        ),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column(
        "state_incarceration_period_history",
        "specialized_purpose_for_incarceration_raw_text",
    )
    op.drop_column(
        "state_incarceration_period_history", "specialized_purpose_for_incarceration"
    )
    op.drop_column(
        "state_incarceration_period", "specialized_purpose_for_incarceration_raw_text"
    )
    op.drop_column(
        "state_incarceration_period", "specialized_purpose_for_incarceration"
    )
    specialized_purpose_for_incarceration = postgresql.ENUM(
        "SHOCK_INCARCERATION",
        "TREATMENT_IN_PRISON",
        name="state_specialized_purpose_for_incarceration",
    )
    specialized_purpose_for_incarceration.drop(op.get_bind())
    # ### end Alembic commands ###
