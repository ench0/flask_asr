"""empty message

Revision ID: 93c3cb484861
Revises: None
Create Date: 2016-11-01 13:12:04.979911

"""

# revision identifiers, used by Alembic.
revision = '93c3cb484861'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('entry', sa.Column('status', sa.SmallInteger(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('entry', 'status')
    ### end Alembic commands ###
