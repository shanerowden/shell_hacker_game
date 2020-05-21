"""empty message

Revision ID: b460772b026d
Revises: f1ceff7eea09
Create Date: 2020-05-17 07:16:58.584421

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b460772b026d'
down_revision = 'f1ceff7eea09'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('character_sheet', 'attr_a')
    op.drop_column('character_sheet', 'attr_c')
    op.drop_column('character_sheet', 'attr_b')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('character_sheet', sa.Column('attr_b', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('character_sheet', sa.Column('attr_c', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('character_sheet', sa.Column('attr_a', sa.INTEGER(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
