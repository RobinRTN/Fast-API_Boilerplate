"""Optionnal fields in the channel table and added the search query

Revision ID: 40f0bd67eb65
Revises: ba126a905adc
Create Date: 2024-12-19 10:18:05.110968

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '40f0bd67eb65'
down_revision = 'ba126a905adc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('channels', schema=None) as batch_op:
        batch_op.add_column(sa.Column('search', sa.Text(), nullable=True))
        batch_op.alter_column('user_id',
               existing_type=sa.INTEGER(),
               nullable=True)
        batch_op.drop_constraint('channels_main_category_id_key', type_='unique')
        batch_op.drop_constraint('channels_sub_category_id_key', type_='unique')
        batch_op.create_index(batch_op.f('ix_channels_main_category_id'), ['main_category_id'], unique=False)
        batch_op.create_index(batch_op.f('ix_channels_sub_category_id'), ['sub_category_id'], unique=False)
        batch_op.create_index(batch_op.f('ix_channels_user_id'), ['user_id'], unique=False)
        batch_op.create_unique_constraint(None, ['name'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('channels', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')
        batch_op.drop_index(batch_op.f('ix_channels_user_id'))
        batch_op.drop_index(batch_op.f('ix_channels_sub_category_id'))
        batch_op.drop_index(batch_op.f('ix_channels_main_category_id'))
        batch_op.create_unique_constraint('channels_sub_category_id_key', ['sub_category_id'])
        batch_op.create_unique_constraint('channels_main_category_id_key', ['main_category_id'])
        batch_op.alter_column('user_id',
               existing_type=sa.INTEGER(),
               nullable=False)
        batch_op.drop_column('search')

    # ### end Alembic commands ###
