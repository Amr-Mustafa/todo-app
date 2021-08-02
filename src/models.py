from flask import Flask, jsonify
from __main__ import bcrypt, database
from config import BCRYPT_LOG_ROUNDS
import uuid


class UserModel():

	def __init__(self, email, password):
		
		self.email = email
		self.email_confirmed = False
		self.password = bcrypt.generate_password_hash(password, BCRYPT_LOG_ROUNDS).decode('utf-8')

	def sign_up(self):
		user = { 'email': self.email, 'password': self.password, 'email_confirmed': self.email_confirmed }
		database.users.insert_one(user)

	@classmethod
	def find_by_username(cls, username):
		return cls.query.filter_by(username=username).first()