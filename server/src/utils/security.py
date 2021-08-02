from src.models import UserModel


def authenticate(email, password):
	user = UserModel(email, password)
	if user.login():
		return user

def identity(payload):
	_id = payload['identity']
	return UserModel.find_by_id(_id)
