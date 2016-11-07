import os

class Configuration(object):
		APPLICATION_DIR = os.path.dirname(os.path.realpath(__file__))
		DEBUG = True
		SECRET_KEY = 'nfhq3fGVVEKVqwgjioqjihg2' # Create a unique key for your app.
		SQLALCHEMY_DATABASE_URI = 'sqlite:///%s/app.db' % APPLICATION_DIR
		SQLALCHEMY_TRACK_MODIFICATIONS = False # to suppress the warning
		# SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:secretpassword@localhost:5432/app_db'
		# pip install psycopg2