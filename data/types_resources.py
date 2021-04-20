from flask import jsonify
from flask_restful import reqparse, abort, Resource
from . import db_session
from .tasks import Task
from .types import Type
api_parser = reqparse.RequestParser()
api_parser.add_argument('api_key', required=True)

parser = reqparse.RequestParser()
parser.add_argument('id', type=int)
parser.add_argument('title',required=True, type=str)

def abort_if_type_not_found(type_id):
    session = db_session.create_session()
    type = session.query(Type).get(type_id)
    if not type:
        abort(404, message=f"Type {type_id} not found")

def abort_if_api_key_is_wrong():
    api_key = api_parser.parse_args()['api_key']
    if api_key != open('data/current_api_key.txt', 'r').readline():
        abort(404,message=f"api key is wrong")

class TypeResource(Resource):
    def get(self, type_id):
        abort_if_api_key_is_wrong()
        abort_if_type_not_found(type_id)
        session = db_session.create_session()
        type = session.query(Type).get(type_id)
        return jsonify({'type': type.to_dict(
            only=('id', 'title'))})

    def delete(self, type_id):
        abort_if_api_key_is_wrong()
        abort_if_type_not_found(type_id)
        session = db_session.create_session()
        type = session.query(Type).get(type_id)
        first_founded_type = session.query(Type).filter(Type.id != type_id).first()
        if first_founded_type:
            for task in type.tasks:
                first_founded_type.tasks.append(task)
                type.tasks.remove(task)
                task.type = first_founded_type.id
            session.delete(type)
        else:
            abort(404,message='last type can not be deleted')
        session.commit()
        return jsonify({'success': 'OK'})

class TypesListResource(Resource):
    def get(self):
        abort_if_api_key_is_wrong()
        session = db_session.create_session()
        types = session.query(Type).all()
        return jsonify({'types': [item.to_dict(
            only=('id','title')) for item in types]})

    def post(self):
        abort_if_api_key_is_wrong()
        args = parser.parse_args()
        session = db_session.create_session()
        if session.query(Type).filter(Type.title == args['title']).first():
            abort(404, message=f'type {args["title"]} is already exist')
        type = Type(title=args['title'])
        session.add(type)
        session.commit()
        return jsonify({'success': 'OK'})

    def patch(self):
        abort_if_api_key_is_wrong()
        args = parser.parse_args()
        session = db_session.create_session()
        if not args['id']:
            abort(404, message='id not found')
        if session.query(Type).filter(Type.title == args['title']).first():
            abort(404, message=f'type {args["title"]} is already exist')
        type = session.query(Type).get(args['id'])
        type.title = args['title']
        session.commit()
        return jsonify({'success': 'OK'})