from flask_admin import Admin
#from flask.ext.admin import Admin #depreciated
# pip install Flask-Admin
from flask_admin.contrib.sqla import ModelView

from app import app, db
from models import Post, Tag, User

admin = Admin(app, 'Blog Admin')
admin.add_view(ModelView(Post, db.session))
admin.add_view(ModelView(Tag, db.session))
admin.add_view(ModelView(User, db.session))
