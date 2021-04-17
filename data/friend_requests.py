import sqlalchemy
from flask_login import UserMixin
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

from data.db_session import SqlAlchemyBase
from werkzeug.security import generate_password_hash, check_password_hash
class FriendRequest(SqlAlchemyBase, UserMixin,SerializerMixin):
    __tablename__ = 'friend_requests'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    sended_by = sqlalchemy.Column(sqlalchemy.Integer)
    received_by = sqlalchemy.Column(sqlalchemy.Integer)

