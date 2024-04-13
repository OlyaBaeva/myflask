"""email

Revision ID: 76470015a839
Revises: f7b3a22a82bf
Create Date: 2024-04-12 13:45:32.891272

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '76470015a839'
down_revision = 'f7b3a22a82bf'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('answers', schema=None) as batch_op:
        batch_op.drop_constraint('answers_email_key', type_='unique')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('answers', schema=None) as batch_op:
        batch_op.create_unique_constraint('answers_email_key', ['email'])

    # ### end Alembic commands ###