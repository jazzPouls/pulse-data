"""add_is_life_to_sentence_group

Revision ID: 964cfd6c3d6c
Revises: 04d24a2daa0b
Create Date: 2019-09-03 19:01:12.272021

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '964cfd6c3d6c'
down_revision = '04d24a2daa0b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('state_sentence_group', sa.Column('is_life', sa.Boolean(), nullable=True))
    op.add_column('state_sentence_group_history', sa.Column('is_life', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('state_sentence_group_history', 'is_life')
    op.drop_column('state_sentence_group', 'is_life')
    # ### end Alembic commands ###
