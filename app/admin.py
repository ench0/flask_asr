from flask_admin import Admin
#from flask.ext.admin import Admin #depreciated
# pip install Flask-Admin
from flask_admin.contrib.sqla import ModelView

from app import app, db
from models import Post, Tag, User

class PostModelView(ModelView):
    column_list = [
        'title', 'status', 'author', 'tease', 'tag_list',
        'created_timestamp',
    ]
    column_select_related_list = ['author'] # Efficiently SELECT the author.

admin = Admin(app, 'Blog Admin')
admin.add_view(PostModelView(Post, db.session))
admin.add_view(ModelView(Tag, db.session))
admin.add_view(ModelView(User, db.session))