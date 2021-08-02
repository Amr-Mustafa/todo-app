from __main__ import app
from flask import render_template, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email, Length
from src.models import UserModel
from src.utils.email import send_email
from src.utils.validators import Unique


class EmailPasswordForm(FlaskForm):
	email = StringField('email', validators=[DataRequired(), Email(), Unique()])
	password = PasswordField('password', validators=[DataRequired(), Length(min=6)])

@app.route('/register', methods=['GET', 'POST'])
def register():
	form = EmailPasswordForm()
	if form.validate_on_submit():
		UserModel(form.email.data, form.password.data).sign_up()
		return redirect(url_for('login'))
	return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
	form = EmailPasswordForm()
	if form.validate_on_submit():
		print(f'email: {form.email.data}, password: {form.password.data}')
	return render_template('login.html', form=form)

@app.route('/dashboard')
def dashboard():
	return 'Dashboard'

