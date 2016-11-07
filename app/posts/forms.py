import wtforms

from models import Post

class PostForm(wtforms.Form):
    title = wtforms.StringField('Title')
    body = wtforms.TextAreaField('Body')
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