from flask import Flask, request, jsonify
from flask_restful import Resource, Api, reqparse

from flask_jwt_extended import JWTManager
from flask_jwt_extended import jwt_required
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity

from flask_bcrypt import Bcrypt
from flask_cors import CORS, cross_origin
from http import HTTPStatus

import smtplib
import pymongo

from bson.json_util import dumps
from bson.objectid import ObjectId

from config import MONGO_PORT

app = Flask(__name__)
api = Api(app)

# Enable Cross-Origin Resource Sharing
CORS(app, resources={r"/*": {"origins": "*"}})

# Password Security
bcrypt = Bcrypt(app)

# Establish connection with the MongoDB database server
client = pymongo.MongoClient('mongodb://admin:password@mongodb')
database = client.todo_app_store

# Application Security
app.config["JWT_SECRET_KEY"] = "super-secret"
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

        database.items.find_one_and_update({'_id': ObjectId(data['_id']), 'email': logged_in_email}, 
            {'$set': {'description': data['description']}})
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
            database.users.insert_one({'email': data['email'], 'password': data['password']})
            return {'msg': 'success'}, HTTPStatus.CREATED.value

        return {'msg': 'fail'}, HTTPStatus.BAD_REQUEST.value 

class Login(Resource):

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('email', type=str, required=True)
        parser.add_argument('password', type=str, required=True)

        data = parser.parse_args()
        user = database.users.find_one({'email': data['email']})

        if user and user['password'] == data['password']:
            access_token = create_access_token(identity=data['email'])
            return access_token, HTTPStatus.OK.value

        return {'msg': 'fail'}, HTTPStatus.BAD_REQUEST.value 

class Ping(Resource):

    def get(self):
        return {'msg': 'pong!'}, HTTPStatus.OK.value

api.add_resource(Ping, '/ping')
api.add_resource(Items, '/items')
api.add_resource(Item, '/item')
api.add_resource(Register, '/register')
api.add_resource(Login, '/login')

if __name__=='__main__':
	app.run(port=8000, debug=True, host='0.0.0.0')
