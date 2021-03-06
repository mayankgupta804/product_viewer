"""Remove Product model + refactor FileMetaData model

Revision ID: e369b4caab45
Revises: 
Create Date: 2019-05-10 11:38:34.610261

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e369b4caab45'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('file_meta_data',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('filename', sa.String(length=64), nullable=True),
    sa.Column('path', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_file_meta_data_filename'), 'file_meta_data', ['filename'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_file_meta_data_filename'), table_name='file_meta_data')
    op.drop_table('file_meta_data')
    # ### end Alembic commands ###
