import datetime

import sqlalchemy
from flask_login import UserMixin
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

from data.db_session import SqlAlchemyBase
from werkzeug.security import generate_password_hash, check_password_hash


class Task(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'tasks'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    creator_id = sqlalchemy.Column(sqlalchemy.Integer,
                                   sqlalchemy.ForeignKey("users.id"))
    creator = orm.relation('User')
    title = sqlalchemy.Column(sqlalchemy.String)
    type = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("types.id"))
    description = sqlalchemy.Column(sqlalchemy.String)
    participating = sqlalchemy.Column(sqlalchemy.String)
    date = sqlalchemy.Column(sqlalchemy.DateTime)
    address = sqlalchemy.Column(sqlalchemy.String)
    country = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("countries.id"))
    is_private = sqlalchemy.Column(sqlalchemy.Boolean)
    is_address_displayed = sqlalchemy.Column(sqlalchemy.Boolean)


    def get_participates_list(self):
        return list(map(int, list(filter(lambda x: x != '', self.participating.split(', ')))))

    def set_participates(self,array):
        self.participating = ', '.join(list(map(str, array)))
