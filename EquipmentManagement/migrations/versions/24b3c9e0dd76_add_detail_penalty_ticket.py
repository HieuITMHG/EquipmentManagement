"""add detail penalty ticket

Revision ID: 24b3c9e0dd76
Revises: ea951704a934
Create Date: 2025-02-03 14:55:47.610670

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '24b3c9e0dd76'
down_revision = 'ea951704a934'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('detail_penalty_ticket',
    sa.Column('penalty_ticket_id', sa.String(length=10), nullable=False),
    sa.Column('violation_id', sa.String(length=10), nullable=False),
    sa.ForeignKeyConstraint(['penalty_ticket_id'], ['penalty_ticket.id'], ),
    sa.ForeignKeyConstraint(['violation_id'], ['violation.id'], ),
    sa.PrimaryKeyConstraint('penalty_ticket_id', 'violation_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('detail_penalty_ticket')
    # ### end Alembic commands ###
