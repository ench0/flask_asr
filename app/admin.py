from flask_admin import Admin
#from flask.ext.admin import Admin #depreciated
# pip install Flask-Admin
from flask_admin.contrib.sqla import ModelView

from app import app, db
from models import Post, Tag, User

class PostModelView(ModelView):
    _status_choices = [(choice, label) for choice, label in [
        (Post.STATUS_PUBLIC, 'Public'),
        (Post.STATUS_DRAFT, 'Draft'),
        (Post.STATUS_DELETED, 'Deleted'),
    ]]
    column_choices = {
        'status': _status_choices,
    }

    column_list = [
        'title', 'status', 'author', 'tease', 'tag_list',
        'created_timestamp',
    ]
    column_select_related_list = ['author'] # Efficiently SELECT the author.


class UserModelView(ModelView):
    column_list = ['email', 'name', 'active', 'created_timestamp']

# Be sure to use the UserModelView class when registering the User:
admin.add_view(UserModelView(User, db.session))


admin = Admin(app, 'Blog Admin')
admin.add_view(PostModelView(Post, db.session))
admin.add_view(ModelView(Tag, db.session))
admin.add_view(ModelView(User, db.session))