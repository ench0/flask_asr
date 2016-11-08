from flask_admin import Admin
#from flask.ext.admin import Admin #depreciated
# pip install Flask-Admin
from flask_admin.contrib.sqla import ModelView

from app import app, db
from models import Post, Tag, User
from wtforms.fields import SelectField # At top of module.
from wtforms.fields import PasswordField # At top of module.

class PostModelView(ModelView):
    _status_choices = [(choice, label) for choice, label in [
        (Post.STATUS_PUBLIC, 'Public'),
        (Post.STATUS_DRAFT, 'Draft'),
        (Post.STATUS_DELETED, 'Deleted'),
    ]]
    column_choices = {
        'status': _status_choices,
    }
    column_filters = [
    'status', User.name, User.email, 'created_timestamp'
    ]
    column_list = [
        'title', 'status', 'author', 'tease', 'tag_list',
        'created_timestamp',
    ]
    column_searchable_list = ['title', 'body']
    column_select_related_list = ['author'] # Efficiently SELECT the author.
    form_args = {
        'status': {'choices': _status_choices, 'coerce': int},
    }
    form_columns = ['title', 'body', 'status', 'author', 'tags']
    form_extra_fields = {
        'password': PasswordField('New password'),
        }
    def on_model_change(self, form, model, is_created):
        if form.password.data:
            model.password_hash = User.make_password(form.password.data)
        return super(UserModelView, self).on_model_change(form, model, is_created)
    form_overrides = {'status': SelectField}
    form_ajax_refs = {
        'author': {
            'fields': (User.name, User.email),
        },
    }


class UserModelView(ModelView):
    column_list = ['email', 'name', 'active', 'created_timestamp']




admin = Admin(app, 'Blog Admin')
admin.add_view(PostModelView(Post, db.session))
admin.add_view(ModelView(Tag, db.session))
admin.add_view(ModelView(User, db.session))

# Be sure to use the UserModelView class when registering the User:
#admin.add_view(UserModelView(User, db.session))