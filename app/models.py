import datetime, re
from app import db

# converts to nice urls
def slugify(s):
	return re.sub('[^\w]+', '-', s).lower()

post_tags = db.Table('post_tags',
	db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')),
	db.Column('post_id', db.Integer, db.ForeignKey('post.id'))
)

class Post(db.Model):
	STATUS_PUBLIC = 0
	STATUS_DRAFT = 1

	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(100))
	slug = db.Column(db.String(100), unique=True)
	body = db.Column(db.Text)
	status = db.Column(db.SmallInteger, default=STATUS_PUBLIC)
	created_timestamp = db.Column(db.DateTime, default=datetime.datetime.now)
	modified_timestamp = db.Column(
		db.DateTime,
		default=datetime.datetime.now,
		onupdate=datetime.datetime.now)

	tags = db.relationship('Tag', secondary=post_tags,
		backref=db.backref('posts', lazy='dynamic'))

	def __init__(self, *args, **kwargs):
		super(Post, self).__init__(*args, **kwargs) # Call parent constructor.
		self.generate_slug()

	def generate_slug(self):
		self.slug = ''
		if self.title:
			self.slug = slugify(self.title)

	def __repr__(self):
		return '<Post: %s>' % self.title
	# the __repr__ method that is used to generate a helpful
	# representation of instances of our Post class. The specific meaning of __repr__
	# is not important but allows you to reference the object that the program is working
	# with, when debugging


class Tag(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(64))
	slug = db.Column(db.String(64), unique=True)

	def __init__(self, *args, **kwargs):
		super(Tag, self).__init__(*args, **kwargs)
		self.slug = slugify(self.name)

	def __repr__(self):
		return '<Tag %s>' % self.name