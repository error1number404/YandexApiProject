import sqlalchemy
from flask_login import UserMixin
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

from data.db_session import SqlAlchemyBase
from werkzeug.security import generate_password_hash, check_password_hash

task_to_user = sqlalchemy.Table(
    'task_to_user',
    SqlAlchemyBase.metadata,
    sqlalchemy.Column('task', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('tasks.id')),
    sqlalchemy.Column('user', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('users.id'))
)

class User(SqlAlchemyBase, UserMixin,SerializerMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    surname = sqlalchemy.Column(sqlalchemy.String)
    name = sqlalchemy.Column(sqlalchemy.String)
    date_of_birth = sqlalchemy.Column(sqlalchemy.DateTime)
    email = sqlalchemy.Column(sqlalchemy.String, unique=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String)
    city_from = sqlalchemy.Column(sqlalchemy.String)
    country_from = sqlalchemy.Column(sqlalchemy.Integer)
    friends = sqlalchemy.Column(sqlalchemy.String,default='')
    tasks = orm.relation("Task",
                           secondary="task_to_user",
                           backref="users")
    creator = orm.relation("Task", back_populates='creator')

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)

    def get_friends_list(self):
        return list(map(int,list(filter(lambda x: x != '', self.friends.split(', ')))))

    def set_friends(self, array):
        self.friends = ', '.join(list(map(str, array)))