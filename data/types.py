import datetime

import sqlalchemy
from flask_login import UserMixin
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

from data.db_session import SqlAlchemyBase
from werkzeug.security import generate_password_hash, check_password_hash

task_to_type = sqlalchemy.Table(
    'task_to_type',
    SqlAlchemyBase.metadata,
    sqlalchemy.Column('task', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('tasks.id')),
    sqlalchemy.Column('type', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('types.id'))
)

class Type(SqlAlchemyBase, UserMixin,SerializerMixin):
    __tablename__ = 'types'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, unique=True)
    tasks = orm.relation("Task",
                         secondary="task_to_type",
                         backref="types")