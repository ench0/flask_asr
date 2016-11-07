import wtforms
from wtforms.validators import DataRequired

from models import Post

from models import Tag
class TagField(wtforms.StringField):
    def _value(self):
        if self.data:
            # Display tags as a comma-separated list.
            return ', '.join([tag.name for tag in self.data])
        return ''

    def get_tags_from_string(self, tag_string):
        raw_tags = tag_string.split(',')
        # Filter out any empty tag names.
        tag_names = [name.strip() for name in raw_tags if name.strip()]
        # Query the database and retrieve any tags we have already saved.
        existing_tags = Tag.query.filter(Tag.name.in_(tag_names))
        # Determine which tag names are new.
        new_names = set(tag_names) - set([tag.name for tag in existing_tags])
        # Create a list of unsaved Tag instances for the new tags.
        new_tags = [Tag(name=name) for name in new_names]
        # Return all the existing tags + all the new, unsaved tags.
        return list(existing_tags) + new_tags

    def process_formdata(self, valuelist):
        if valuelist:
            self.data = self.get_tags_from_string(valuelist[0])
        else:
            self.data = []


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
    tags = TagField(
        'Tags',
        description='Separate multiple tags with commas.')

    def save_post(self, post):
        self.populate_obj(post)
        post.generate_slug()
        return post


class ImageForm(wtforms.Form):
    file = wtforms.FileField('Image file')