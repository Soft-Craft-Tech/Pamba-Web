"""empty message

Revision ID: 2e2f346c401b
Revises: 6ed8aeb8a14f
Create Date: 2024-03-17 21:00:36.799710

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2e2f346c401b'
down_revision = '6ed8aeb8a14f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('services_businesses_association', schema=None) as batch_op:
        batch_op.add_column(sa.Column('price', sa.Integer(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('services_businesses_association', schema=None) as batch_op:
        batch_op.drop_column('price')

    # ### end Alembic commands ###
