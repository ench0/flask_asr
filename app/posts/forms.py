import wtforms
from wtforms.validators import DataRequired

from models import Post


class PostForm(wtforms.Form):
    title = wtforms.StringField(
        'Title',
        validators=[DataRequired()])
    body = wtforms.TextAreaField(
        'Body',
        validators=[DataRequired()])
    status = wtforms.SelectField(
        'Post status',
        choices=(
            (Post.STATUS_PUBLIC, 'Public'),
            (Post.STATUS_DRAFT, 'Draft')),
        coerce=int)

    def save_post(self, post):
        self.populate_obj(post)
        post.generate_slug()
        return post