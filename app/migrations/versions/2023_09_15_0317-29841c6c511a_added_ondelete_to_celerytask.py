"""added ondelete to CeleryTask

Revision ID: 29841c6c511a
Revises: d7af124def0b
Create Date: 2023-09-15 03:17:24.024516

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '29841c6c511a'
down_revision: Union[str, None] = 'd7af124def0b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('celery_tasks_task_id_fkey', 'celery_tasks', type_='foreignkey')
    op.create_foreign_key(None, 'celery_tasks', 'tasks', ['task_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'celery_tasks', type_='foreignkey')
    op.create_foreign_key('celery_tasks_task_id_fkey', 'celery_tasks', 'tasks', ['task_id'], ['id'])
    # ### end Alembic commands ###