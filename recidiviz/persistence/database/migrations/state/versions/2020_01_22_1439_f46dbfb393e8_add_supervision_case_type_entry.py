# pylint: skip-file
"""add_supervision_case_type_entry

Revision ID: f46dbfb393e8
Revises: 035c280cf168
Create Date: 2020-01-22 14:39:19.936397

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "f46dbfb393e8"
down_revision = "035c280cf168"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "state_supervision_case_type_entry",
        sa.Column(
            "case_type",
            sa.Enum(
                "DOMESTIC_VIOLENCE",
                "GENERAL",
                "SERIOUS_MENTAL_ILLNESS",
                "SEX_OFFENDER",
                name="state_supervision_case_type",
            ),
            nullable=True,
        ),
        sa.Column("case_type_raw_text", sa.String(length=255), nullable=True),
        sa.Column("state_code", sa.String(length=255), nullable=False),
        sa.Column("supervision_case_type_entry_id", sa.Integer(), nullable=False),
        sa.Column("supervision_period_id", sa.Integer(), nullable=True),
        sa.Column("person_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["person_id"],
            ["state_person.person_id"],
            initially="DEFERRED",
            deferrable=True,
        ),
        sa.ForeignKeyConstraint(
            ["supervision_period_id"],
            ["state_supervision_period.supervision_period_id"],
        ),
        sa.PrimaryKeyConstraint("supervision_case_type_entry_id"),
    )
    op.create_index(
        op.f("ix_state_supervision_case_type_entry_person_id"),
        "state_supervision_case_type_entry",
        ["person_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_state_supervision_case_type_entry_state_code"),
        "state_supervision_case_type_entry",
        ["state_code"],
        unique=False,
    )
    op.create_index(
        op.f("ix_state_supervision_case_type_entry_supervision_period_id"),
        "state_supervision_case_type_entry",
        ["supervision_period_id"],
        unique=False,
    )
    op.create_table(
        "state_supervision_case_type_entry_history",
        sa.Column("valid_from", sa.DateTime(), nullable=False),
        sa.Column("valid_to", sa.DateTime(), nullable=True),
        sa.Column(
            "case_type",
            sa.Enum(
                "DOMESTIC_VIOLENCE",
                "GENERAL",
                "SERIOUS_MENTAL_ILLNESS",
                "SEX_OFFENDER",
                name="state_supervision_case_type",
            ),
            nullable=True,
        ),
        sa.Column("case_type_raw_text", sa.String(length=255), nullable=True),
        sa.Column("state_code", sa.String(length=255), nullable=False),
        sa.Column(
            "supervision_case_type_entry_history_id", sa.Integer(), nullable=False
        ),
        sa.Column("supervision_case_type_entry_id", sa.Integer(), nullable=False),
        sa.Column("supervision_period_id", sa.Integer(), nullable=True),
        sa.Column("person_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["person_id"],
            ["state_person.person_id"],
            initially="DEFERRED",
            deferrable=True,
        ),
        sa.ForeignKeyConstraint(
            ["supervision_case_type_entry_id"],
            ["state_supervision_case_type_entry.supervision_case_type_entry_id"],
        ),
        sa.ForeignKeyConstraint(
            ["supervision_period_id"],
            ["state_supervision_period.supervision_period_id"],
        ),
        sa.PrimaryKeyConstraint("supervision_case_type_entry_history_id"),
    )
    op.create_index(
        op.f("ix_state_supervision_case_type_entry_history_person_id"),
        "state_supervision_case_type_entry_history",
        ["person_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_state_supervision_case_type_entry_history_state_code"),
        "state_supervision_case_type_entry_history",
        ["state_code"],
        unique=False,
    )
    op.create_index(
        op.f(
            "ix_state_supervision_case_type_entry_history_supervision_case_type_entry_id"
        ),
        "state_supervision_case_type_entry_history",
        ["supervision_case_type_entry_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_state_supervision_case_type_entry_history_supervision_period_id"),
        "state_supervision_case_type_entry_history",
        ["supervision_period_id"],
        unique=False,
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(
        op.f("ix_state_supervision_case_type_entry_history_supervision_period_id"),
        table_name="state_supervision_case_type_entry_history",
    )
    op.drop_index(
        op.f(
            "ix_state_supervision_case_type_entry_history_supervision_case_type_entry_id"
        ),
        table_name="state_supervision_case_type_entry_history",
    )
    op.drop_index(
        op.f("ix_state_supervision_case_type_entry_history_state_code"),
        table_name="state_supervision_case_type_entry_history",
    )
    op.drop_index(
        op.f("ix_state_supervision_case_type_entry_history_person_id"),
        table_name="state_supervision_case_type_entry_history",
    )
    op.drop_table("state_supervision_case_type_entry_history")
    op.drop_index(
        op.f("ix_state_supervision_case_type_entry_supervision_period_id"),
        table_name="state_supervision_case_type_entry",
    )
    op.drop_index(
        op.f("ix_state_supervision_case_type_entry_state_code"),
        table_name="state_supervision_case_type_entry",
    )
    op.drop_index(
        op.f("ix_state_supervision_case_type_entry_person_id"),
        table_name="state_supervision_case_type_entry",
    )
    op.drop_table("state_supervision_case_type_entry")

    op.execute("DROP TYPE state_supervision_case_type;")
    # ### end Alembic commands ###
