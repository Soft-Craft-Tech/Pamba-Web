"""Add place id character limit

Revision ID: 407b33d725ec
Revises: e3e99fe38745
Create Date: 2025-06-03 13:29:32.171550

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '407b33d725ec'
down_revision = 'e3e99fe38745'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('businesses', schema=None) as batch_op:
        batch_op.alter_column('place_id',
               existing_type=sa.VARCHAR(length=100),
               type_=sa.String(length=1000),
               existing_nullable=True)


    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###

    with op.batch_alter_table('businesses', schema=None) as batch_op:
        batch_op.alter_column('place_id',
               existing_type=sa.String(length=1000),
               type_=sa.VARCHAR(length=100),
               existing_nullable=True)

    # ### end Alembic commands ###
