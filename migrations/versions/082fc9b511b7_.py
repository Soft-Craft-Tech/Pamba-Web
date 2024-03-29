"""empty message

Revision ID: 082fc9b511b7
Revises: eca0634ae06c
Create Date: 2024-03-14 12:02:36.484802

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '082fc9b511b7'
down_revision = 'eca0634ae06c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('clients', schema=None) as batch_op:
        batch_op.add_column(sa.Column('otp_expiration', sa.DateTime(), nullable=True))
        batch_op.alter_column('otp',
               existing_type=sa.VARCHAR(length=300),
               type_=sa.String(length=15),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('clients', schema=None) as batch_op:
        batch_op.alter_column('otp',
               existing_type=sa.String(length=15),
               type_=sa.VARCHAR(length=300),
               existing_nullable=True)
        batch_op.drop_column('otp_expiration')

    # ### end Alembic commands ###
