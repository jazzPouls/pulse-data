# pylint: skip-file
"""supervision_contacts

Revision ID: 4f84ccf378b8
Revises: 8651414e971f
Create Date: 2020-06-15 16:14:18.074579

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "4f84ccf378b8"
down_revision = "8651414e971f"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "state_supervision_contact",
        sa.Column("external_id", sa.String(length=255), nullable=True),
        sa.Column("state_code", sa.String(length=255), nullable=False),
        sa.Column("contact_date", sa.Date(), nullable=True),
        sa.Column(
            "contact_reason",
            sa.Enum(
                "INTERNAL_UNKNOWN",
                "EXTERNAL_UNKNOWN",
                "EMERGENCY_CONTACT",
                "GENERAL_CONTACT",
                "INITIAL_CONTACT",
                name="state_supervision_contact_reason",
            ),
            nullable=True,
        ),
        sa.Column("contact_reason_raw_text", sa.String(length=255), nullable=True),
        sa.Column(
            "contact_type",
            sa.Enum(
                "INTERNAL_UNKNOWN",
                "EXTERNAL_UNKNOWN",
                "FACE_TO_FACE",
                "TELEPHONE",
                "WRITTEN_MESSAGE",
                name="state_supervision_contact_type",
            ),
            nullable=True,
        ),
        sa.Column("contact_type_raw_text", sa.String(length=255), nullable=True),
        sa.Column(
            "location",
            sa.Enum(
                "INTERNAL_UNKNOWN",
                "EXTERNAL_UNKNOWN",
                "COURT",
                "FIELD",
                "JAIL",
                "PLACE_OF_EMPLOYMENT",
                "RESIDENCE",
                "SUPERVISION_OFFICE",
                "TREATMENT_PROVIDER",
                name="state_supervision_contact_location",
            ),
            nullable=True,
        ),
        sa.Column("location_raw_text", sa.String(length=255), nullable=True),
        sa.Column("resulted_in_arrest", sa.Boolean(), nullable=True),
        sa.Column(
            "status",
            sa.Enum(
                "INTERNAL_UNKNOWN",
                "EXTERNAL_UNKNOWN",
                "ATTEMPTED",
                "COMPLETED",
                name="state_supervision_contact_status",
            ),
            nullable=True,
        ),
        sa.Column("status_raw_text", sa.String(length=255), nullable=True),
        sa.Column("verified_employment", sa.Boolean(), nullable=True),
        sa.Column("supervision_contact_id", sa.Integer(), nullable=False),
        sa.Column("contacted_agent_id", sa.Integer(), nullable=True),
        sa.Column("person_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["contacted_agent_id"],
            ["state_agent.agent_id"],
        ),
        sa.ForeignKeyConstraint(
            ["person_id"],
            ["state_person.person_id"],
            initially="DEFERRED",
            deferrable=True,
        ),
        sa.PrimaryKeyConstraint("supervision_contact_id"),
    )
    op.create_index(
        op.f("ix_state_supervision_contact_contacted_agent_id"),
        "state_supervision_contact",
        ["contacted_agent_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_state_supervision_contact_external_id"),
        "state_supervision_contact",
        ["external_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_state_supervision_contact_person_id"),
        "state_supervision_contact",
        ["person_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_state_supervision_contact_state_code"),
        "state_supervision_contact",
        ["state_code"],
        unique=False,
    )
    op.create_table(
        "state_supervision_contact_history",
        sa.Column("valid_from", sa.DateTime(), nullable=False),
        sa.Column("valid_to", sa.DateTime(), nullable=True),
        sa.Column("external_id", sa.String(length=255), nullable=True),
        sa.Column("state_code", sa.String(length=255), nullable=False),
        sa.Column("contact_date", sa.Date(), nullable=True),
        sa.Column(
            "contact_reason",
            sa.Enum(
                "INTERNAL_UNKNOWN",
                "EXTERNAL_UNKNOWN",
                "EMERGENCY_CONTACT",
                "GENERAL_CONTACT",
                "INITIAL_CONTACT",
                name="state_supervision_contact_reason",
            ),
            nullable=True,
        ),
        sa.Column("contact_reason_raw_text", sa.String(length=255), nullable=True),
        sa.Column(
            "contact_type",
            sa.Enum(
                "INTERNAL_UNKNOWN",
                "EXTERNAL_UNKNOWN",
                "FACE_TO_FACE",
                "TELEPHONE",
                "WRITTEN_MESSAGE",
                name="state_supervision_contact_type",
            ),
            nullable=True,
        ),
        sa.Column("contact_type_raw_text", sa.String(length=255), nullable=True),
        sa.Column(
            "location",
            sa.Enum(
                "INTERNAL_UNKNOWN",
                "EXTERNAL_UNKNOWN",
                "COURT",
                "FIELD",
                "JAIL",
                "PLACE_OF_EMPLOYMENT",
                "RESIDENCE",
                "SUPERVISION_OFFICE",
                "TREATMENT_PROVIDER",
                name="state_supervision_contact_location",
            ),
            nullable=True,
        ),
        sa.Column("location_raw_text", sa.String(length=255), nullable=True),
        sa.Column("resulted_in_arrest", sa.Boolean(), nullable=True),
        sa.Column(
            "status",
            sa.Enum(
                "INTERNAL_UNKNOWN",
                "EXTERNAL_UNKNOWN",
                "ATTEMPTED",
                "COMPLETED",
                name="state_supervision_contact_status",
            ),
            nullable=True,
        ),
        sa.Column("status_raw_text", sa.String(length=255), nullable=True),
        sa.Column("verified_employment", sa.Boolean(), nullable=True),
        sa.Column("supervision_contact_history_id", sa.Integer(), nullable=False),
        sa.Column("supervision_contact_id", sa.Integer(), nullable=False),
        sa.Column("contacted_agent_id", sa.Integer(), nullable=True),
        sa.Column("person_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["contacted_agent_id"],
            ["state_agent.agent_id"],
        ),
        sa.ForeignKeyConstraint(
            ["person_id"],
            ["state_person.person_id"],
            initially="DEFERRED",
            deferrable=True,
        ),
        sa.ForeignKeyConstraint(
            ["supervision_contact_id"],
            ["state_supervision_contact.supervision_contact_id"],
        ),
        sa.PrimaryKeyConstraint("supervision_contact_history_id"),
    )
    op.create_index(
        op.f("ix_state_supervision_contact_history_contacted_agent_id"),
        "state_supervision_contact_history",
        ["contacted_agent_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_state_supervision_contact_history_external_id"),
        "state_supervision_contact_history",
        ["external_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_state_supervision_contact_history_person_id"),
        "state_supervision_contact_history",
        ["person_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_state_supervision_contact_history_state_code"),
        "state_supervision_contact_history",
        ["state_code"],
        unique=False,
    )
    op.create_index(
        op.f("ix_state_supervision_contact_history_supervision_contact_id"),
        "state_supervision_contact_history",
        ["supervision_contact_id"],
        unique=False,
    )
    op.create_table(
        "state_supervision_period_supervision_contact_association",
        sa.Column("supervision_period_id", sa.Integer(), nullable=True),
        sa.Column("supervision_contact_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["supervision_contact_id"],
            ["state_supervision_contact.supervision_contact_id"],
        ),
        sa.ForeignKeyConstraint(
            ["supervision_period_id"],
            ["state_supervision_period.supervision_period_id"],
        ),
    )
    op.create_index(
        op.f(
            "ix_state_supervision_period_supervision_contact_association_supervision_period_id"
        ),
        "state_supervision_period_supervision_contact_association",
        ["supervision_period_id"],
        unique=False,
    )
    op.create_index(
        op.f(
            "ix_state_supervision_period_supervision_contact_association_supervision_contact_id"
        ),
        "state_supervision_period_supervision_contact_association",
        ["supervision_contact_id"],
        unique=False,
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(
        op.f(
            "ix_state_supervision_period_supervision_contact_association_supervision_contact_id"
        ),
        table_name="state_supervision_period_supervision_contact_association",
    )
    op.drop_index(
        op.f(
            "ix_state_supervision_period_supervision_contact_association_supervision_period_id"
        ),
        table_name="state_supervision_period_supervision_contact_association",
    )
    op.drop_table("state_supervision_period_supervision_contact_association")
    op.drop_index(
        op.f("ix_state_supervision_contact_history_supervision_contact_id"),
        table_name="state_supervision_contact_history",
    )
    op.drop_index(
        op.f("ix_state_supervision_contact_history_state_code"),
        table_name="state_supervision_contact_history",
    )
    op.drop_index(
        op.f("ix_state_supervision_contact_history_person_id"),
        table_name="state_supervision_contact_history",
    )
    op.drop_index(
        op.f("ix_state_supervision_contact_history_external_id"),
        table_name="state_supervision_contact_history",
    )
    op.drop_index(
        op.f("ix_state_supervision_contact_history_contacted_agent_id"),
        table_name="state_supervision_contact_history",
    )
    op.drop_table("state_supervision_contact_history")
    op.drop_index(
        op.f("ix_state_supervision_contact_state_code"),
        table_name="state_supervision_contact",
    )
    op.drop_index(
        op.f("ix_state_supervision_contact_person_id"),
        table_name="state_supervision_contact",
    )
    op.drop_index(
        op.f("ix_state_supervision_contact_external_id"),
        table_name="state_supervision_contact",
    )
    op.drop_index(
        op.f("ix_state_supervision_contact_contacted_agent_id"),
        table_name="state_supervision_contact",
    )
    op.drop_table("state_supervision_contact")

    op.execute("DROP TYPE state_supervision_contact_status;")
    op.execute("DROP TYPE state_supervision_contact_location;")
    op.execute("DROP TYPE state_supervision_contact_type;")
    op.execute("DROP TYPE state_supervision_contact_reason;")
    # ### end Alembic commands ###
