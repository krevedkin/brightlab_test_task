"""added unique constraint to TaskUser

Revision ID: 951374136c25
Revises: 7cd158c555f3
Create Date: 2023-09-14 02:05:34.317541

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '951374136c25'
down_revision: Union[str, None] = '7cd158c555f3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'tasks_users', ['user_id', 'task_id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'tasks_users', type_='unique')
    # ### end Alembic commands ###
