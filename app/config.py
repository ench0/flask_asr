import os

class Configuration(object):
		APPLICATION_DIR = os.path.dirname(os.path.realpath(__file__))
		DEBUG = True
		SQLALCHEMY_DATABASE_URI = 'sqlite:///%s/blog.db' % APPLICATION_DIR
		SQLALCHEMY_TRACK_MODIFICATIONS = False # to suppress the warning
		# SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:secretpassword@localhost:5432/blog_db'
		# pip install psycopg2