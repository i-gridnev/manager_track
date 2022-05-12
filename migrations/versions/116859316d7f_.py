"""empty message

Revision ID: 116859316d7f
Revises: a740233ae1ba
Create Date: 2022-05-10 17:19:56.527625

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '116859316d7f'
down_revision = 'a740233ae1ba'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('task', 'created_at',
               existing_type=mysql.DATETIME(),
               nullable=True)
    op.drop_column('task', 'updated_at')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('task', sa.Column('updated_at', mysql.DATETIME(), nullable=True))
    op.alter_column('task', 'created_at',
               existing_type=mysql.DATETIME(),
               nullable=False)
    # ### end Alembic commands ###