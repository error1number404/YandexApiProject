from flask import jsonify
from flask_restful import reqparse, abort, Resource
from . import db_session
from .friend_requests import FriendRequest
from .users import User

api_parser = reqparse.RequestParser()
api_parser.add_argument('api_key', required=True)

parser = reqparse.RequestParser()
parser.add_argument('id', type=int)
parser.add_argument('sended_by', type=int)
parser.add_argument('received_by', type=int)


def abort_if_friend_request_not_found(friend_request_id):
    session = db_session.create_session()
    friend_request = session.query(FriendRequest).get(friend_request_id)
    if not friend_request:
        abort(404, message=f"Friend request {friend_request_id} not found")


def abort_if_user_not_found(user_id):
    session = db_session.create_session()
    user = session.query(User).get(user_id)
    if not user:
        abort(404, message=f"User {user_id} not found")


def abort_if_api_key_is_wrong():
    api_key = api_parser.parse_args()['api_key']
    if api_key != open('data/current_api_key.txt', 'r').readline():
        abort(404, message=f"api key is wrong")


class FriendRequestResource(Resource):
    def get(self, friend_request_id):
        abort_if_api_key_is_wrong()
        abort_if_friend_request_not_found(friend_request_id)
        session = db_session.create_session()
        friend_request = session.query(FriendRequest).get(friend_request_id)
        return jsonify({'friend_request': friend_request.to_dict(
            only=('id', 'sended_by', 'received_by'))})

    def delete(self, friend_request_id):
        abort_if_api_key_is_wrong()
        abort_if_friend_request_not_found(friend_request_id)
        session = db_session.create_session()
        friend_request = session.query(FriendRequest).get(friend_request_id)
        session.delete(friend_request)
        session.commit()
        return jsonify({'success': 'OK'})


class FriendRequestsListResource(Resource):
    def get(self):
        abort_if_api_key_is_wrong()
        session = db_session.create_session()
        friend_requests = session.query(FriendRequest).all()
        return jsonify({'friend_requests': [item.to_dict(
            only=('id', 'sended_by', 'received_by')) for item in friend_requests]})

    def post(self):
        abort_if_api_key_is_wrong()
        args = parser.parse_args()
        session = db_session.create_session()
        if None in [args[key] for key in args][1:]:
            abort(404,
                  message=f'Missing keys: {", ".join(list(filter(lambda x: (args[x] is None and x != "id"), [key for key in args])))}')
        abort_if_user_not_found(args['sended_by'])
        abort_if_user_not_found(args['received_by'])
        if args['sended_by'] == args['received_by']:
            abort(404, message='sended_by can not be equals received_by')
        if session.query(FriendRequest).filter(FriendRequest.sended_by == args['received_by'],
                                               FriendRequest.received_by == args['sended_by']).first() or session.query(
                FriendRequest).filter(FriendRequest.sended_by == args['sended_by'],
                                      FriendRequest.received_by == args['received_by']).first():
            abort(404, message='Friend request like that already exist')
        friend_request = FriendRequest(sended_by=args['sended_by'],
                                       received_by=args['received_by'])
        session.add(friend_request)
        session.commit()
        return jsonify({'success': 'OK'})

    def patch(self):
        abort_if_api_key_is_wrong()
        args = parser.parse_args()
        session = db_session.create_session()
        if not args['id']:
            abort(404, message='id not found')
        if len(list(filter(bool, [args[key] for key in args]))) == 1:
            abort(404, message='fields for edit not found')
        friend_request = session.query(FriendRequest).get(args['id'])
        if args['sended_by']:
            abort_if_user_not_found(args['sended_by'])
            if args['sended_by'] == friend_request.received_by:
                abort(404, message='sended_by can not be equals received_by')
            if session.query(FriendRequest).filter(FriendRequest.sended_by == friend_request.received_by,
                                                   FriendRequest.received_by == args[
                                                       'sended_by']).first() or session.query(FriendRequest).filter(
                FriendRequest.sended_by == args['sended_by'],
                FriendRequest.received_by == friend_request.received_by).first():
                abort(404, message='Friend request like that already exist')
            friend_request.sended_by = args['sended_by']
        if args['received_by']:
            abort_if_user_not_found(args['received_by'])
            if args['received_by'] == friend_request.sended_by:
                abort(404, message='sended_by can not be equals received_by')
            if session.query(FriendRequest).filter(FriendRequest.sended_by == friend_request.sended_by,
                                                   FriendRequest.received_by == args[
                                                       'received_by']).first() or session.query(FriendRequest).filter(
                FriendRequest.sended_by == args['received_by'],
                FriendRequest.received_by == friend_request.sended_by).first():
                abort(404, message='Friend request like that already exist')
            friend_request.received_by = args['received_by']
        session.commit()
        return jsonify({'success': 'OK'})
