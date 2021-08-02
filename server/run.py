from flask import Flask, render_template
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt

import smtplib
import pymongo

from instance.config import EMAIL_ADDRESS, EMAIL_PASSWORD
from config import MONGO_PORT

app = Flask(__name__, template_folder='./src/templates/')
app.config.from_object('instance.config.DevelopmentConfig')

# Password Security
bcrypt = Bcrypt(app)

# MongoDB Connection
client = pymongo.MongoClient('localhost', MONGO_PORT)
database = client.todo_app_store

# Application Security
jwt = JWTManager(app)

# Mail Server Connection
# mail_server = smtplib.SMTP(host='smtp-mail.outlook.com', port=587)

from src.views import register

@app.route('/')
def index():
	return render_template('index.html')

if __name__=='__main__':
	# mail_server.starttls()
	# mail_server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
	app.run(port=8080, debug=True)