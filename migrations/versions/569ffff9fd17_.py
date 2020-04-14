"""empty message

Revision ID: 569ffff9fd17
Revises: dce6b6fc8553
Create Date: 2020-04-14 08:17:34.501403

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '569ffff9fd17'
down_revision = 'dce6b6fc8553'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user', 'is_email_public',
               existing_type=sa.BOOLEAN(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user', 'is_email_public',
               existing_type=sa.BOOLEAN(),
               nullable=True)
    # ### end Alembic commands ###