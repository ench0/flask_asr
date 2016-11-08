from flask_admin import Admin
#from flask.ext.admin import Admin #depreciated
# pip install Flask-Admin
from app import app

admin = Admin(app, 'Blog Admin')