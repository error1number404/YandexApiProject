import datetime

import sqlalchemy
from flask_login import UserMixin
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

from data.db_session import SqlAlchemyBase
from werkzeug.security import generate_password_hash, check_password_hash

task_to_country = sqlalchemy.Table(
    'task_to_country',
    SqlAlchemyBase.metadata,
    sqlalchemy.Column('task', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('tasks.id')),
    sqlalchemy.Column('country', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('countries.id'))
)

class Country(SqlAlchemyBase, UserMixin,SerializerMixin):
    __tablename__ = 'countries'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String,unique=True)
    tasks = orm.relation("Task",
                         secondary="task_to_country",
                         backref="countries")