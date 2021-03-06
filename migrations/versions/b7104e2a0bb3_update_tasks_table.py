"""update tasks table

Revision ID: b7104e2a0bb3
Revises: 8afbd4758e80
Create Date: 2019-05-30 12:31:38.668817

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'b7104e2a0bb3'
down_revision = '8afbd4758e80'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tasks', sa.Column('created_at', sa.DateTime(timezone=True), nullable=True))
    op.add_column('tasks', sa.Column('failure_ttl', sa.Integer(), nullable=True))
    op.add_column('tasks', sa.Column('result_ttl', sa.Integer(), nullable=True))
    op.add_column('tasks', sa.Column('timeout', sa.Integer(), nullable=True))
    op.add_column('tasks', sa.Column('ttl', sa.Integer(), nullable=True))
    op.alter_column('tasks', 'started_at',
               existing_type=postgresql.TIMESTAMP(timezone=True),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('tasks', 'started_at',
               existing_type=postgresql.TIMESTAMP(timezone=True),
               nullable=False)
    op.drop_column('tasks', 'ttl')
    op.drop_column('tasks', 'timeout')
    op.drop_column('tasks', 'result_ttl')
    op.drop_column('tasks', 'failure_ttl')
    op.drop_column('tasks', 'created_at')
    # ### end Alembic commands ###
