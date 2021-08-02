from flask import Flask, jsonify
from __main__ import bcrypt, database
from config import BCRYPT_LOG_ROUNDS


class UserModel():

	def __init__(self, email, password):
		
		self.email = email
		self.email_confirmed = False
		self.password = bcrypt.generate_password_hash(password, BCRYPT_LOG_ROUNDS).decode('utf-8')
		self.todo_items = []

	def signup(self):
		user = { 'email': self.email, 'password': self.password, 'email_confirmed': self.email_confirmed }
		database.users.insert_one(user)

	@classmethod
	def login(cls, email, plaintext_password):
		user = database.users.find_one({ 'email': email })
		return user and bcrypt.check_password_hash(user['password'], plaintext_password)

class ToDoItem():
	
	def __init__(self, items):
		self.items = items
