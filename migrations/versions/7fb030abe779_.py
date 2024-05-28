"""empty message

Revision ID: 7fb030abe779
Revises: 8ffad8353266
Create Date: 2024-05-16 10:37:43.925469

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7fb030abe779'
down_revision = '8ffad8353266'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('reserve',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.Column('email', sa.String(length=200), nullable=False),
    sa.Column('since', sa.TIMESTAMP(), nullable=True),
    sa.Column('forend', sa.TIMESTAMP(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    with op.batch_alter_table('reserve', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_reserve_id'), ['id'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('reserve', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_reserve_id'))

    op.drop_table('reserve')
    # ### end Alembic commands ###