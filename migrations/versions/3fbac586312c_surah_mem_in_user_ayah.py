"""surah_mem in user_ayah


Revision ID: 3fbac586312c
Revises: 8fb71ba7a6b9
Create Date: 2024-11-04 00:45:43.682979

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3fbac586312c'
down_revision = '907758551b47'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('ayah', schema=None) as batch_op:
        batch_op.alter_column('timestamp_memorized',
               existing_type=sa.INTEGER(),
               nullable=True)

    with op.batch_alter_table('memorization_user_ayah', schema=None) as batch_op:
        batch_op.alter_column('timestamp_memorized',
               existing_type=sa.INTEGER(),
               nullable=True)
        batch_op.alter_column('surah_memorized',
               existing_type=sa.INTEGER(),
               nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('memorization_user_ayah', schema=None) as batch_op:
        batch_op.alter_column('surah_memorized',
               existing_type=sa.INTEGER(),
               nullable=False)
        batch_op.alter_column('timestamp_memorized',
               existing_type=sa.INTEGER(),
               nullable=True)

    with op.batch_alter_table('ayah', schema=None) as batch_op:
        batch_op.alter_column('timestamp_memorized',
               existing_type=sa.INTEGER(),
               nullable=True)

    # ### end Alembic commands ###
