import datetime, re
from app import db, bcrypt, login_manager

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
	STATUS_DELETED = 2

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

	author_id = db.Column(db.Integer, db.ForeignKey("user.id"))

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

	@property
	def tag_list(self):
		return ', '.join(tag.name for tag in self.tags)
	@property
	def tease(self):
		return self.body[:100]





# tags
class Tag(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(64))
	slug = db.Column(db.String(64), unique=True)

	def __init__(self, *args, **kwargs):
		super(Tag, self).__init__(*args, **kwargs)
		self.slug = slugify(self.name)

	def __repr__(self):
		return '<Tag %s>' % self.name

# users
class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(64), unique=True)
	password_hash = db.Column(db.String(255))
	name = db.Column(db.String(64))
	slug = db.Column(db.String(64), unique=True)
	active = db.Column(db.Boolean, default=True)
	admin = db.Column(db.Boolean, default=False)
	created_timestamp = db.Column(db.DateTime, default=datetime.datetime.now)
	posts = db.relationship('Post', backref='author', lazy='dynamic')
	def __init__(self, *args, **kwargs):
		super(User, self).__init__(*args, **kwargs)
		self.generate_slug()
	def generate_slug(self):
		if self.name:
			self.slug = slugify(self.name)

	# Flask-Login interface..
	def get_id(self):
		return str(self.id) #return str(self.id, 'utf-8')
	def is_authenticated(self):
		return True
	def is_active(self):
		return self.active
	def is_anonymous(self):
		return False

	@staticmethod
	def make_password(plaintext):
		return bcrypt.generate_password_hash(plaintext)
	def check_password(self, raw_password):
		return bcrypt.check_password_hash(self.password_hash, raw_password)
	@classmethod
	def create(cls, email, password, **kwargs):
		return User(email=email, password_hash=User.make_password(password), **kwargs)
	@staticmethod
	def authenticate(email, password):
		user = User.query.filter(User.email == email).first()
		if user and user.check_password(password):
			return user
		return False


@login_manager.user_loader
def _user_loader(user_id):
	return User.query.get(int(user_id))