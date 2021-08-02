EMAIL_ADDRESS = 'amr.mustafa.97@outlook.com'
EMAIL_PASSWORD = '9192631770TacticalDood'


class Config(object):
	DEBUG = False
	TESTING = False
	SECRET_KEY = 'my_secret!'

class ProductionConfig(Config):
	pass

class DevelopmentConfig(Config):
	DEBUG = True

class TestingConfig(Config):
	TESTING = True
