from flask import Flask, render_template
from instance.config import EMAIL_ADDRESS, EMAIL_PASSWORD
from config import MONGO_PORT
from flask_bcrypt import Bcrypt
import smtplib
import pymongo

app = Flask(__name__, template_folder='./src/templates/')
app.config.from_object('instance.config.DevelopmentConfig')

bcrypt = Bcrypt(app)
client = pymongo.MongoClient('localhost', MONGO_PORT)
database = client.todo_app_store

# mail_server = smtplib.SMTP(host='smtp-mail.outlook.com', port=587)

from src.views import register

@app.route('/')
def index():
	return render_template('index.html')

if __name__=='__main__':
	# mail_server.starttls()
	# mail_server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
	app.run(port=8080, debug=True)