"""Initial migration

Revision ID: 8716b03cbf27
Revises: 
Create Date: 2024-09-27 12:34:51.154223

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8716b03cbf27'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('confirm')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('confirm', sa.VARCHAR(length=50), autoincrement=False, nullable=True))

    # ### end Alembic commands ###
