import os
import json
import requests

from datetime import timedelta

from flask import Flask
from flask import jsonify
from flask import redirect
from flask import request
from flask import url_for
from flask import make_response

from flask_restful import Resource
from flask_restful import Api
from flask_restful import reqparse

from flask_jwt_extended import JWTManager
from flask_jwt_extended import jwt_required
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import get_jwt

from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_dance.contrib.github import make_github_blueprint, github
from flask_sse import sse

import pymongo
from http import HTTPStatus
from bson.objectid import ObjectId

from config import MONGO_PORT
from config import BCRYPT_LOG_ROUNDS
from config import SECRET_KEY

app = Flask(__name__)
app.secret_key = 'dontlook'
api = Api(app)

github_blueprint = make_github_blueprint(
        client_id='cb72d955c84365f9f932',
        client_secret='86d3bacf3f3f414e82826a19e4eafcddbc670a67',
        redirect_url='http://localhost:8080/'
)
app.register_blueprint(github_blueprint, url_prefix='/login')        

# Enable Cross-Origin Resource Sharing
CORS(app, resources={r"/*": {"origins": "*"}})

# Password Security
bcrypt = Bcrypt(app)

# Establish connection with the MongoDB database server
client = pymongo.MongoClient('localhost', MONGO_PORT)
username = os.environ['ME_CONFIG_MONGODB_ADMINUSERNAME']
password = os.environ['ME_CONFIG_MONGODB_ADMINPASSWORD']
url = os.environ['ME_CONFIG_MONGODB_SERVER']
#client = pymongo.MongoClient(f'mongodb://{username}:{password}@{url}')

try:
    pass
    client.admin.command('ping')
except Exception:
    print("Server not available")

database = client.todo_app_store

# Application Security
app.config["JWT_SECRET_KEY"] = SECRET_KEY
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
jwt = JWTManager(app)

@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
    jti = jwt_payload['jti']
    return True if database.revokedTokens.find_one({'jti': jti}) else False

# Server-Side Events
app.config["REDIS_URL"] = "redis://localhost"
app.register_blueprint(sse, url_prefix='/stream')

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


class GithubLogin(Resource):

    def get(self):
        payload = {
            'client_secret': '86d3bacf3f3f414e82826a19e4eafcddbc670a67',
            'client_id': 'cb72d955c84365f9f932',
            'redirect_uri': 'http://localhost:8000/api/login/github',
            'code': request.args.get('code')
        }
        headers = {'Accept': 'application/json'}
        resp = requests.post('https://github.com/login/oauth/access_token', headers=headers, params=payload)
        github_access_token = resp.json()['access_token']

        headers = {
            'Authorization': f'token {github_access_token}',
            'Accept': 'application/json'
        }
        resp = requests.get('https://api.github.com/user', headers=headers)
        email = resp.json()['email']

        if database.users.find_one({'email': email}):
            api_access_token = create_access_token(identity=email)
            sse.publish({'email': email, 'jwt': api_access_token}, type='auth')
            return {'msg': 'success'}, HTTPStatus.OK.value
        else:
            return {'msg': f'user {email} not found'}, HTTPStatus.BAD_REQUEST.value

class Logout(Resource):

    @jwt_required()
    def delete(self):
        resp = make_response(jsonify({'msg': 'JWT revoked'}))
        if github.authorized:
            resp.set_cookie('session', '', expires=0)
        jti = get_jwt()['jti']
        database.revokedTokens.insert_one({'jti': jti})
        return resp



class Ping(Resource):

    def get(self):
        if not github.authorized:
            return redirect(url_for('github.login'))
        resp = github.get('/user')
        assert resp.ok
        return {'msg': 'pong!'}, HTTPStatus.OK.value

api.add_resource(Ping, '/api/ping')
api.add_resource(Items, '/api/items')
api.add_resource(Item, '/api/item')
api.add_resource(Register, '/api/register')
api.add_resource(Login, '/api/login')
api.add_resource(GithubLogin, '/api/login/github')
api.add_resource(Logout, '/api/logout')

if __name__=='__main__':
	app.run(port=8000, debug=True, host='0.0.0.0')
