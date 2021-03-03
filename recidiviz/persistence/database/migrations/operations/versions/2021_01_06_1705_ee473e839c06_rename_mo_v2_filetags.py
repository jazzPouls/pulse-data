# pylint: skip-file
"""rename_mo_v2_filetags

Revision ID: ee473e839c06
Revises: 106493b6e763
Create Date: 2021-01-06 17:05:16.103547

"""
from alembic import op


# revision identifiers, used by Alembic.
revision = "ee473e839c06"
down_revision = "106493b6e763"
branch_labels = None
depends_on = None


UPDATE_MO_FILE_TAGS_QUERY = (
    "UPDATE direct_ingest_ingest_file_metadata"
    " SET file_tag = SUBSTRING(file_tag, 1, LENGTH(file_tag) - 3)"
    " WHERE region_code = 'US_MO';"
)


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    connection = op.get_bind()  # type: ignore [attr-defined]
    connection.execute(UPDATE_MO_FILE_TAGS_QUERY)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    connection = op.get_bind()  # type: ignore [attr-defined]
    connection.execute(
        "UPDATE direct_ingest_ingest_file_metadata"
        " SET file_tag = CONCAT(file_tag, '_v2')"
        " WHERE region_code = 'US_MO';"
    )
    # ### end Alembic commands ###
