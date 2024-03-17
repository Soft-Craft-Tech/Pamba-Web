"""empty message

Revision ID: 153a51af918c
Revises: 71ee93840c4b
Create Date: 2024-03-17 22:46:27.844179

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '153a51af918c'
down_revision = '71ee93840c4b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('services_businesses_association', schema=None) as batch_op:
        batch_op.add_column(sa.Column('business_id', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('service_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(None, 'businesses', ['business_id'], ['id'])
        batch_op.create_foreign_key(None, 'services', ['service_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('services_businesses_association', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('service_id')
        batch_op.drop_column('business_id')

    # ### end Alembic commands ###