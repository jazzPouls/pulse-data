"""remove_name_and_parole_cols

Revision ID: 711e0ee2a7c4
Revises: a434e2fa0724
Create Date: 2019-08-21 19:33:19.220185

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "711e0ee2a7c4"
down_revision = "a434e2fa0724"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("state_parole_decision", "received_parole")
    op.drop_column("state_parole_decision_history", "received_parole")
    op.drop_column("state_person_alias", "middle_names")
    op.drop_column("state_person_alias", "given_names")
    op.drop_column("state_person_alias", "name_suffix")
    op.drop_column("state_person_alias", "surname")
    op.drop_column("state_person_alias_history", "middle_names")
    op.drop_column("state_person_alias_history", "given_names")
    op.drop_column("state_person_alias_history", "name_suffix")
    op.drop_column("state_person_alias_history", "surname")
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "state_person_alias_history",
        sa.Column(
            "surname", sa.VARCHAR(length=255), autoincrement=False, nullable=True
        ),
    )
    op.add_column(
        "state_person_alias_history",
        sa.Column(
            "name_suffix", sa.VARCHAR(length=255), autoincrement=False, nullable=True
        ),
    )
    op.add_column(
        "state_person_alias_history",
        sa.Column(
            "given_names", sa.VARCHAR(length=255), autoincrement=False, nullable=True
        ),
    )
    op.add_column(
        "state_person_alias_history",
        sa.Column(
            "middle_names", sa.VARCHAR(length=255), autoincrement=False, nullable=True
        ),
    )
    op.add_column(
        "state_person_alias",
        sa.Column(
            "surname", sa.VARCHAR(length=255), autoincrement=False, nullable=True
        ),
    )
    op.add_column(
        "state_person_alias",
        sa.Column(
            "name_suffix", sa.VARCHAR(length=255), autoincrement=False, nullable=True
        ),
    )
    op.add_column(
        "state_person_alias",
        sa.Column(
            "given_names", sa.VARCHAR(length=255), autoincrement=False, nullable=True
        ),
    )
    op.add_column(
        "state_person_alias",
        sa.Column(
            "middle_names", sa.VARCHAR(length=255), autoincrement=False, nullable=True
        ),
    )
    op.add_column(
        "state_parole_decision_history",
        sa.Column("received_parole", sa.BOOLEAN(), autoincrement=False, nullable=True),
    )
    op.add_column(
        "state_parole_decision",
        sa.Column("received_parole", sa.BOOLEAN(), autoincrement=False, nullable=True),
    )
    # ### end Alembic commands ###
