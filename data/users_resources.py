import datetime

from flask import jsonify,request
from flask_restful import reqparse, abort,  Resource
from . import db_session
from .tasks import Task
from .friend_requests import FriendRequest
from validate_email import validate_email
from .users import User
api_parser = reqparse.RequestParser()
api_parser.add_argument('api_key', required=True)

parser = reqparse.RequestParser()
parser.add_argument('id', type=int)
parser.add_argument('surname')
parser.add_argument('name')
parser.add_argument('date_of_birth')
parser.add_argument('password')
parser.add_argument('email')
parser.add_argument('city_from')
parser.add_argument('country_from',type=int)
parser.add_argument('friends',type=int, action='append')

def abort_if_user_not_found(user_id):
    session = db_session.create_session()
    user = session.query(User).get(user_id)
    if not user:
        abort(404, message=f"User {user_id} not found")

def abort_if_users_not_found(users_id):
    session = db_session.create_session()
    users_not_found = []
    for user in [session.query(User).get(user_id) for user_id in users_id]:
        if not user:
            users_not_found.append(user.id)
    if users_not_found:
        abort(404, message=f"Users: {','.join(users_not_found)} not found")

def abort_if_api_key_is_wrong():
    api_key = api_parser.parse_args()['api_key']
    if api_key != open('data/current_api_key.txt', 'r').readline():
        abort(404,message=f"api key is wrong")

class UserResource(Resource):
    def get(self, user_id):
        abort_if_api_key_is_wrong()
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        return jsonify({'user': user.to_dict(
            only=('id','surname', 'name','email', 'date_of_birth', 'city_from', 'country_from', 'friends'))})

    def delete(self, user_id):
        abort_if_api_key_is_wrong()
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        for item in [session.query(User).get(friend_id) for friend_id in user.get_friends_list()]:
            friends = item.get_friends_list()
            friends.remove(user.id)
            item.set_friends(friends)
        for task in user.tasks:
            if user != task.creator:
                participating = task.get_participates_list()
                participating.remove(user.id)
                task.set_participates(participating)
            elif user == task.creator and task.participating:
                new_creator = session.query(User).get(task.get_participates_list()[0])
                task.creator = new_creator
                task.creator_id = new_creator.id
                task.set_participates(task.get_participates_list()[1:])
            elif user == task.creator and not task.participating:
                session.delete(task)
        for friend_request in session.query(FriendRequest).filter((FriendRequest.sended_by == user.id) | (FriendRequest.received_by == user.id)):
            session.delete(friend_request)
        session.delete(user)
        session.commit()
        return jsonify({'success': 'OK'})

class UsersListResource(Resource):
    def get(self):
        abort_if_api_key_is_wrong()
        session = db_session.create_session()
        users = session.query(User).all()
        return jsonify({'users': [item.to_dict(
            only=('id','surname', 'name','email', 'date_of_birth', 'city_from', 'country_from', 'friends')) for item in users]})

    def post(self):
        abort_if_api_key_is_wrong()
        args = parser.parse_args()
        json_request = request.json
        session = db_session.create_session()
        if [args[key] for key in args][1:].count(None) > 1 or (not args['friends'] and 'friends' not in json_request):
            abort(404,
                  message=f'Missing keys: {", ".join(list(filter(lambda x: (args[x] is None and x != "id") and x not in json_request, [key for key in args])))}')
        if session.query(User).filter(User.email == args['email']).first():
            abort(404, message=f'email {args["email"]} is already used')
        try:
            date = datetime.datetime.strptime(args['date_of_birth'], '%Y-%m-%d')
        except ValueError:
            abort(404, message='Wrong date_of_birth format. Use format like that: 2000-01-01')
        if not validate_email(args['email']):
            abort(404, message='Wrong email format. Use format like that: example@domen.com')
        abort_if_users_not_found(args['friends'])
        user = User(name=args['name'],
                    surname=args['surname'],
                    date_of_birth=datetime.datetime.strptime(args['date_of_birth'], '%Y-%m-%d'),
                    email=args['email'],
                    city_from=args['city_from'],
                    country_from=args['country_from'])
        if not args['friends'] and 'friends' in json_request:
            args['friends'] = []
        user.set_friends(args['friends'])
        user.set_password(args['password'])
        session.add(user)
        for item in [session.query(User).get(friend_id) for friend_id in args['friends']]:
            item.set_friends(item.get_friends_list()+[user.id])
        session.commit()
        return jsonify({'success': 'OK'})

    def patch(self):
        abort_if_api_key_is_wrong()
        args = parser.parse_args()
        json_request = request.json
        if not args['id']:
            abort(404, message='id not found')
        if len(list(filter(bool,[args[key] for key in args]))) == 1 and 'friends' not in json_request:
            abort(404, message='fields for edit not found')
        abort_if_user_not_found(args['id'])
        session = db_session.create_session()
        if args['email']:
            if session.query(User).filter(User.email == args['email']).first():
                abort(404, message=f'email {args["email"]} is already used')
        if args['date_of_birth']:
            try:
                date = datetime.datetime.strptime(args['date_of_birth'], '%Y-%m-%d')
            except ValueError:
                abort(404, message='Wrong date_of_birth format. Use format like that: 2000-01-01')
        user = session.query(User).get(args['id'])
        if not args['friends'] and 'friends' in json_request:
            args['friends'] = []
        if args['friends'] is not None:
            abort_if_users_not_found(args['friends'])
            for item in [session.query(User).get(friend_id) for friend_id in user.get_friends_list()]:
                friends = item.get_friends_list()
                friends.remove(user.id)
                item.set_friends(friends)
            user.set_friends(args['friends'])
            for item in [session.query(User).get(friend_id) for friend_id in args['friends']]:
                item.set_friends(item.get_friends_list() + [user.id])
        if args['name']:
            user.name = args['name']
        if args['surname']:
            user.surname = args['surname']
        if args['date_of_birth']:
            user.date_of_birth = datetime.datetime.strptime(args['date_of_birth'], '%Y-%m-%d')
        if args['email']:
            if not validate_email(args['email']):
                abort(404, message='Wrong email format. Use format like that: example@domen.com')
            user.email = args['email']
        if args['city_from']:
            user.city_from = args['city_from']
        if args['country_from']:
            user.country_from = args['country_from']
        if args['password']:
            user.set_password(args['password'])
        session.commit()
        return jsonify({'success': 'OK'})