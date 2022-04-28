"""empty message

Revision ID: 5b65d8a15fa3
Revises: e52273d2d695
Create Date: 2022-04-27 21:57:05.222672

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '5b65d8a15fa3'
down_revision = 'e52273d2d695'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('member', sa.Column('discordid', sa.String(255), nullable=False))
    op.add_column('member', sa.Column('steamid', sa.String(255), nullable=False))
    op.drop_column('member', 'id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('member', sa.Column('id', mysql.VARCHAR(length=255), nullable=False))
    op.drop_column('member', 'steamid')
    op.drop_column('member', 'discordid')
    # ### end Alembic commands ###