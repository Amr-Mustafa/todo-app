import os

from flask import Flask
from flask import jsonify

from flask_restful import Resource
from flask_restful import Api
from flask_restful import reqparse

from flask_jwt_extended import JWTManager
from flask_jwt_extended import jwt_required
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity

from flask_bcrypt import Bcrypt
from flask_cors import CORS

import pymongo
from http import HTTPStatus
from bson.objectid import ObjectId

from config import MONGO_PORT
from config import BCRYPT_LOG_ROUNDS
from config import SECRET_KEY

app = Flask(__name__)
api = Api(app)

# Enable Cross-Origin Resource Sharing
CORS(app, resources={r"/*": {"origins": "*"}})

# Password Security
bcrypt = Bcrypt(app)

# Establish connection with the MongoDB database server
# client = pymongo.MongoClient('localhost', MONGO_PORT)
username = os.environ['ME_CONFIG_MONGODB_ADMINUSERNAME']
password = os.environ['ME_CONFIG_MONGODB_ADMINPASSWORD']
url = os.environ['ME_CONFIG_MONGODB_SERVER']
client = pymongo.MongoClient(f'mongodb://{username}:{password}@{url}')

try:
    client.admin.command('ping')
except Exception:
    print("Server not available")

database = client.todo_app_store

# Application Security
app.config["JWT_SECRET_KEY"] = SECRET_KEY
jwt = JWTManager(app)


class Item(Resource):

    @jwt_required()
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('description', type=str, required=True)

        logged_in_email = get_jwt_identity()
        data = parser.parse_args()
        item = {
            'email': logged_in_email,
            'description': data['description']
        }

        database.items.insert_one(item)
        return HTTPStatus.OK.value

    @jwt_required()
    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('_id', type=str, required=True)

        logged_in_email = get_jwt_identity()
        data = parser.parse_args()

        database.items.find_one_and_delete({'_id': ObjectId(data['_id']), 'email': logged_in_email})

    @jwt_required()
    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('_id', type=str, required=True)
        parser.add_argument('description', type=str, required=True)

        logged_in_email = get_jwt_identity()
        data = parser.parse_args()

        database.items.find_one_and_update(
            {
            '_id': ObjectId(data['_id']),
            'email': logged_in_email
            },  
            {
                '$set': {
                    'description': data['description']
                }
            }
        )
        return HTTPStatus.OK.value


class Items(Resource):

    @jwt_required()
    def get(self):
        logged_in_email = get_jwt_identity()
        raw_items = database.items.find({'email': logged_in_email})

        items = []
        for item in raw_items:
            items.append({
                '_id': str(item['_id']),
                'email': item['email'],
                'description': item['description']
            })

        return jsonify(items)


class Register(Resource):

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('email', type=str, required=True)
        parser.add_argument('password', type=str, required=True)

        data = parser.parse_args()

        if not database.users.find_one({'email': data['email']}):
            database.users.insert_one({
                    'email': data['email'],
                    'password': bcrypt.generate_password_hash(data['password'], BCRYPT_LOG_ROUNDS).decode('utf-8')
                })
            return {'msg': 'success'}, HTTPStatus.CREATED.value

        return {'msg': 'fail'}, HTTPStatus.BAD_REQUEST.value 


class Login(Resource):

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('email', type=str, required=True)
        parser.add_argument('password', type=str, required=True)

        data = parser.parse_args()
        user = database.users.find_one({'email': data['email']})

        if user and bcrypt.check_password_hash(user['password'], data['password']):
            access_token = create_access_token(identity=data['email'])
            return access_token, HTTPStatus.OK.value

        return {'msg': 'fail'}, HTTPStatus.BAD_REQUEST.value 


class Ping(Resource):

    def get(self):
        return {'msg': 'pong!'}, HTTPStatus.OK.value

api.add_resource(Ping, '/api/ping')
api.add_resource(Items, '/api/items')
api.add_resource(Item, '/api/item')
api.add_resource(Register, '/api/register')
api.add_resource(Login, '/api/login')


if __name__=='__main__':
	app.run(port=8000, debug=True, host='0.0.0.0')
