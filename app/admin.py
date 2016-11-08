from flask import g, url_for
from flask_admin import Admin, AdminIndexView, expose
#from flask.ext.admin import Admin #depreciated
# pip install Flask-Admin
from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib.fileadmin import FileAdmin

from app import app, db
from models import Post, Tag, User, post_tags
from wtforms.fields import SelectField # At top of module.
from wtforms.fields import PasswordField # At top of module.



class AdminAuthentication(object):
    def is_accessible(self):
        return g.user.is_authenticated and g.user.is_admin()


# fixing slugs
class BaseModelView(AdminAuthentication, ModelView):
    pass


class SlugModelView(BaseModelView):
    def on_model_change(self, form, model, is_created):
        model.generate_slug()
        return super(SlugModelView, self).on_model_change(form, model, is_created)


class PostModelView(SlugModelView):
    _status_choices = [(choice, label) for choice, label in [
        (Post.STATUS_PUBLIC, 'Public'),
        (Post.STATUS_DRAFT, 'Draft'),
        (Post.STATUS_DELETED, 'Deleted'),
    ]]
    column_choices = {
        'status': _status_choices,
    }
    column_filters = ['status', User.name, User.email, 'created_timestamp']
    column_list = [
        'title', 'slug', 'status', 'author', 'tease', 'tag_list',
        'created_timestamp',
    ]
    column_searchable_list = ['title', 'body']
    column_select_related_list = ['author']
    form_ajax_refs = {
        'author': {
            'fields': (User.name, User.email),
        },
    }
    form_args = {
        'status': {'choices': _status_choices, 'coerce': int},
    }
    form_columns = ['title', 'body', 'status', 'author', 'tags']
    form_overrides = {'status': SelectField}


class UserModelView(SlugModelView):
    column_filters = ('email', 'name', 'active')#, 'admin'
    column_list = ['email', 'name', 'active', 'created_timestamp']#, 'admin'
    column_searchable_list = ['email', 'name']
    form_columns = ['email', 'password', 'name', 'active']#, 'admin'
    form_extra_fields = {
        'password': PasswordField('New password'),
    }
    def on_model_change(self, form, model, is_created):
        if form.password.data:
            model.password_hash = User.make_password(form.password.data)
        return super(UserModelView, self).on_model_change(form, model, is_created)


class BlogFileAdmin(AdminAuthentication, FileAdmin):
    pass

class IndexView(AdminIndexView):
    @expose('/')
    def index(self):
        if not (g.user.is_authenticated and g.user.is_admin()):
            return redirect(url_for('login', next=request.path))
        return self.render('admin/index.html')

admin = Admin(app, 'Blog Admin', index_view=IndexView())
admin.add_view(PostModelView(Post, db.session))
admin.add_view(SlugModelView(Tag, db.session))
admin.add_view(UserModelView(User, db.session))
admin.add_view(
    BlogFileAdmin(app.config['STATIC_DIR'], '/static/', name='Static Files'))