import datetime
import os

from flask import jsonify,request
from flask_restful import reqparse, abort, Resource
from . import db_session
from .tasks import Task
from .countries import Country
from .types import Type
from .users import User
from .get_map_picture import get_map_picture
api_parser = reqparse.RequestParser()
api_parser.add_argument('api_key', required=True)
parser = reqparse.RequestParser()
parser.add_argument('id', type=int)
parser.add_argument('creator_id', type=int)
parser.add_argument('title')
parser.add_argument('type', type=int)
parser.add_argument('description')
parser.add_argument('participating',type=int, nullable=False, action='append')
parser.add_argument('date')
parser.add_argument('address')
parser.add_argument('country', type=int)
parser.add_argument('is_private', type=bool)
parser.add_argument('is_address_displayed', type=bool)

def abort_if_task_not_found(task_id):
    session = db_session.create_session()
    task = session.query(Task).get(task_id)
    if not task:
        abort(404, message=f"Task {task_id} not found")

def abort_if_api_key_is_wrong():
    api_key = api_parser.parse_args()['api_key']
    if api_key != open('data/current_api_key.txt', 'r').readline():
        abort(404,message=f"api key is wrong")

class TaskResource(Resource):
    def get(self, task_id):
        abort_if_api_key_is_wrong()
        abort_if_task_not_found(task_id)
        session = db_session.create_session()
        task = session.query(Task).get(task_id)
        return jsonify({'task': task.to_dict(
            only=('id','creator_id','title', 'type', 'description', 'participating', 'date', 'address','country','is_private', 'is_address_displayed'))})

    def delete(self, task_id):
        abort_if_api_key_is_wrong()
        abort_if_task_not_found(task_id)
        session = db_session.create_session()
        task = session.query(Task).get(task_id)
        session.delete(task)
        session.commit()
        return jsonify({'success': 'OK'})

class TasksListResource(Resource):
    def get(self):
        abort_if_api_key_is_wrong()
        session = db_session.create_session()
        tasks = session.query(Task).all()
        return jsonify({'tasks': [item.to_dict(
            only=('id','creator_id','title', 'type', 'description', 'participating', 'date', 'address','country','is_private', 'is_address_displayed')) for item in tasks]})

    def post(self):
        abort_if_api_key_is_wrong()
        args = parser.parse_args()
        json_request = request.json
        if [args[key] for key in args][1:].count(None) > 1 or (not args['participating'] and 'participating' not in json_request):
            abort(404, message=f'Missing keys: {", ".join(list(filter(lambda x: (args[x] is None and x != "id") and x not in json_request,[key for key in args])))}')
        try:
            date = datetime.datetime.strptime(args['date'], '%Y-%m-%d %H:%M')
        except ValueError:
            abort(404, message='Wrong date format. Use format like that: 2000-01-01 16:00')
        if args['creator_id'] in args['participating']:
            abort(404, message='Creator can not be in participating')
        session = db_session.create_session()
        task = Task(creator=session.query(User).get(args['creator_id']),
                    creator_id=args['creator_id'],
                    title=args['title'],
                    type=args['type'],
                    description= args['description'],
                    date=datetime.datetime.strptime(args['date'], '%Y-%m-%d %H:%M'),
                    country=args['country'],
                    address=args['address'],
                    is_private=args['is_private'],
                    is_address_displayed=args['is_address_displayed'])
        if not args['participating'] and 'participating' in json_request:
            args['participating'] = []
        task.set_participates(args['participating'])
        session.add(task)
        session.commit()
        type = session.query(Type).get(args['type'])
        country = session.query(Country).get(args['country'])
        type.tasks.append(task)
        country.tasks.append(task)
        for user in list(map(lambda x: session.query(User).get(x), args['participating']+[args['creator_id']])):
            user.tasks.append(task)
        session.commit()

        if task.is_address_displayed:
            get_map_picture(task.id, task.address)

        return jsonify({'success': 'OK'})

    def patch(self):
        abort_if_api_key_is_wrong()
        args = parser.parse_args()
        json_request = request.json
        if not args['id']:
            abort(404, message='id not found')
        if len(list(filter(bool,[args[key] for key in args]))) == 1 and 'participating' not in json_request:
            abort(404, message='fields for edit not found')
        if args['date']:
            try:
                date = datetime.datetime.strptime(args['date'], '%Y-%m-%dT%H:%M')
            except ValueError:
                abort(404, message='Wrong date format. Use format like that: 2000-01-01 16:00')
        session = db_session.create_session()
        abort_if_task_not_found(args['id'])
        task = session.query(Task).get(args['id'])
        if not args['participating'] and 'participating' in json_request:
            args['participating'] = []
        if args['participating'] is not None:
            if task.creator_id in args['participating']:
                abort(404, message='Creator can not be in participating')
            for user in list(map(lambda x: session.query(User).get(x), task.get_participates_list())):
                user.tasks.remove(task)
            task.set_participates(args['participating'])
            for user in list(map(lambda x: session.query(User).get(x), args['participating'])):
                user.tasks.append(task)
        if args['type']:
            type = session.query(Type).get(args['type'])
            type.tasks.remove(task)
            task.type = args['type']
            type = session.query(Type).get(args['type'])
            type.tasks.append(task)
        if args['country']:
            country = session.query(Country).get(args['country'])
            country.tasks.remove(task)
            task.country = args['country']
            country = session.query(Country).get(args['country'])
            country.tasks.append(task)
        if args['creator_id']:
            if args['creator_id'] in task.get_participates_list():
                abort(404, message='Creator can not be in participating')
            cur_creator = session.query(User).get(task.creator_id)
            cur_creator.tasks.remove(task)
            task.creator = session.query(User).get(args['creator_id'])
            task.creator_id = args['creator_id']
        if args['title']:
            task.title = args['title']
        if args['description']:
            task.description = args['description']
        if args['date']:
            task.date = datetime.datetime.strptime(args['date'], '%Y-%m-%dT%H:%M')
        if args['address']:
            task.address = args['address']
        if args['is_private']:
            task.is_private = args['is_private']
        if args['is_address_displayed']:
            task.is_address_displayed = args['is_address_displayed']
            if task.is_address_displayed:
                get_map_picture(task.id, task.address)
            else:
                picture_name_list = os.listdir('static/img')
                if f'{task.id}_map_picture.jpg' in picture_name_list and not task.is_address_displayed:
                    os.remove(f'static/img/{task.id}_map_picture.jpg')
        session.commit()
        return jsonify({'success': 'OK'})