"""empty message

Revision ID: 71ee93840c4b
Revises: 4e0c79cd4975
Create Date: 2024-03-17 22:37:04.210132

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '71ee93840c4b'
down_revision = '4e0c79cd4975'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('services_businesses_association', schema=None) as batch_op:
        batch_op.add_column(sa.Column('id', sa.Integer(), nullable=False))
        batch_op.drop_constraint('services_businesses_association_business_id_fkey', type_='foreignkey')
        batch_op.drop_constraint('services_businesses_association_service_id_fkey', type_='foreignkey')
        batch_op.drop_column('business_id')
        batch_op.drop_column('service_id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('services_businesses_association', schema=None) as batch_op:
        batch_op.add_column(sa.Column('service_id', sa.INTEGER(), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('business_id', sa.INTEGER(), autoincrement=False, nullable=True))
        batch_op.create_foreign_key('services_businesses_association_service_id_fkey', 'services', ['service_id'], ['id'])
        batch_op.create_foreign_key('services_businesses_association_business_id_fkey', 'businesses', ['business_id'], ['id'])
        batch_op.drop_column('id')

    # ### end Alembic commands ###