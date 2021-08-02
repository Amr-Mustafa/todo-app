from __main__ import app, jwt

from flask import render_template, redirect, url_for, jsonify

from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required

from flask_wtf import FlaskForm

from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email, Length

from src.models import UserModel
from src.utils.email import send_email
from src.utils.validators import Unique


class UniqueEmailPasswordForm(FlaskForm):
	email = StringField('email', validators=[DataRequired(), Email(), Unique()])
	password = PasswordField('password', validators=[DataRequired(), Length(min=6)])

class EmailPasswordForm(UniqueEmailPasswordForm):
	email = StringField('email', validators=[DataRequired(), Email()])

@app.route('/register', methods=['GET', 'POST'])
def register():
	form = UniqueEmailPasswordForm()
	if form.validate_on_submit():
		UserModel(form.email.data, form.password.data).signup()
		return redirect(url_for('login'))
	return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
	form = EmailPasswordForm()
	if form.validate_on_submit() and UserModel.login(form.email.data, form.password.data):
		access_token = create_access_token(identity=form.email.data)
		return jsonify(access_token=access_token)
	return render_template('login.html', form=form)

@app.route('/dashboard')
def dashboard():
	user = UserModel('', 'sdfsff')
	user.todo_items.append('first item')
	return render_template('dashboard.html', todo_items=user.todo_items)

