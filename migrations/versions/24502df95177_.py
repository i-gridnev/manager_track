"""empty message

Revision ID: 24502df95177
Revises: bbae9d21065c
Create Date: 2022-05-11 15:19:46.160243

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '24502df95177'
down_revision = 'bbae9d21065c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('task', 'author_id',
               existing_type=mysql.INTEGER(),
               nullable=True)
    op.drop_constraint('task_ibfk_2', 'task', type_='foreignkey')
    op.drop_column('task', 'report_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('task', sa.Column('report_id', mysql.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key('task_ibfk_2', 'task', 'report', ['report_id'], ['id'])
    op.alter_column('task', 'author_id',
               existing_type=mysql.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###
