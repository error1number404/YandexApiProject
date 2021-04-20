from flask import jsonify
from flask_restful import reqparse, abort,Resource
from . import db_session
from .tasks import Task
from .countries import Country
from .users import User
api_parser = reqparse.RequestParser()
api_parser.add_argument('api_key', required=True)

parser = reqparse.RequestParser()
parser.add_argument('id', type=int)
parser.add_argument('name',required=True, type=str)

def abort_if_country_not_found(country_id):
    session = db_session.create_session()
    country = session.query(Country).get(country_id)
    if not country:
        abort(404, message=f"Country {country_id} not found")

def abort_if_api_key_is_wrong():
    api_key = api_parser.parse_args()['api_key']
    if api_key != open('data/current_api_key.txt', 'r').readline():
        abort(404,message=f"api key is wrong")

class CountryResource(Resource):
    def get(self, country_id):
        abort_if_api_key_is_wrong()
        abort_if_country_not_found(country_id)
        session = db_session.create_session()
        country = session.query(Country).get(country_id)
        return jsonify({'country': country.to_dict(
            only=('id', 'name'))})

    def delete(self, country_id):
        abort_if_api_key_is_wrong()
        abort_if_country_not_found(country_id)
        session = db_session.create_session()
        country = session.query(Country).get(country_id)
        first_founded_country = session.query(Country).filter(Country.id != country_id).first()
        if first_founded_country:
            for task in country.tasks:
                first_founded_country.tasks.append(task)
                country.tasks.remove(task)
                task.country = first_founded_country.id
            for user in session.query(User).filter(User.country_from == country_id):
                user.country_from = first_founded_country.id
            session.delete(country)
        else:
            abort(404,message='last country can not be deleted')
        session.commit()
        return jsonify({'success': 'OK'})

class CountriesListResource(Resource):
    def get(self):
        abort_if_api_key_is_wrong()
        session = db_session.create_session()
        countries = session.query(Country).all()
        return jsonify({'countries': [item.to_dict(
            only=('id','name')) for item in countries]})

    def post(self):
        abort_if_api_key_is_wrong()
        args = parser.parse_args()
        session = db_session.create_session()
        if session.query(Country).filter(Country.name == args['name']).first():
            abort(404, message=f'country {args["name"]} is already exist')
        country = Country(name=args['name'])
        session.add(country)
        session.commit()
        return jsonify({'success': 'OK'})

    def patch(self):
        abort_if_api_key_is_wrong()
        args = parser.parse_args()
        session = db_session.create_session()
        if not args['id']:
            abort(404, message='id not found')
        if session.query(Country).filter(Country.name == args['name']).first():
            abort(404, message=f'country {args["name"]} is already exist')
        country = session.query(Country).get(args['id'])
        country.name = args['name']
        session.commit()
        return jsonify({'success': 'OK'})