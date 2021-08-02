from wtforms.validators import ValidationError
from __main__ import bcrypt, database


class Unique(object):
	def __init__(self, message='This element already exists.'):
		self.message = message

	def __call__(self, form, field):
		if database.users.find_one({'email': field.data}):
			raise ValidationError(self.message)