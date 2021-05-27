"""empty message

Revision ID: a274545ebf5b
Revises: 09bc7845118c
Create Date: 2021-05-20 23:02:00.776244

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a274545ebf5b'
down_revision = '09bc7845118c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('profile',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=60), nullable=True),
    sa.Column('link', sa.String(length=200), nullable=True),
    sa.Column('image', sa.String(length=200), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.add_column('products', sa.Column('max_price', sa.Float(), nullable=True))
    op.add_column('products', sa.Column('min_price', sa.Float(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('products', 'min_price')
    op.drop_column('products', 'max_price')
    op.drop_table('profile')
    # ### end Alembic commands ###