# pylint: skip-file
"""user_actions

Revision ID: b67b063f4047
Revises: 6be45427233e
Create Date: 2021-02-03 16:49:30.482648

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "b67b063f4047"
down_revision = "6be45427233e"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "user_actions",
        sa.Column("person_external_id", sa.String(length=255), nullable=False),
        sa.Column("officer_external_id", sa.String(length=255), nullable=False),
        sa.Column("state_code", sa.String(length=255), nullable=False),
        sa.Column(
            "action_metadata", postgresql.JSONB(astext_type=sa.Text()), nullable=False
        ),
        sa.Column(
            "action_ts", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.PrimaryKeyConstraint(
            "person_external_id", "officer_external_id", "state_code"
        ),
    )
    op.create_index(
        op.f("ix_user_actions_officer_external_id"),
        "user_actions",
        ["officer_external_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_user_actions_person_external_id"),
        "user_actions",
        ["person_external_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_user_actions_state_code"), "user_actions", ["state_code"], unique=False
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_user_actions_state_code"), table_name="user_actions")
    op.drop_index(op.f("ix_user_actions_person_external_id"), table_name="user_actions")
    op.drop_index(
        op.f("ix_user_actions_officer_external_id"), table_name="user_actions"
    )
    op.drop_table("user_actions")
    # ### end Alembic commands ###
