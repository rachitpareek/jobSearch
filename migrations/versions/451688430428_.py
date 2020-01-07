"""empty message

Revision ID: 451688430428
Revises: bd37c0f51222
Create Date: 2020-01-07 12:12:20.274528

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '451688430428'
down_revision = 'bd37c0f51222'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('application', sa.Column('last_updated', sa.DateTime(), nullable=True))
    op.create_index(op.f('ix_application_last_updated'), 'application', ['last_updated'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_application_last_updated'), table_name='application')
    op.drop_column('application', 'last_updated')
    # ### end Alembic commands ###
