from flask import Blueprint

from helpers import object_list
from models import Post, Tag

posts = Blueprint('posts', __name__,template_folder='templates')

@posts.route('/')
def index():
    posts = Post.query.order_by(Post.created_timestamp.desc())
    return object_list('posts/index.html', posts)

@posts.route('/tags/')
def tag_index():
    tags = Tag.query.order_by(Tag.name)
    return object_list('posts/tag_index.html', tags)

@posts.route('/tags/<slug>/')
def tag_detail(slug):
    pass

@posts.route('/<slug>/')
def detail(slug):
    entry = Entry.query.filter(Entry.slug == slug).first_or_404()
    return render_template('posts/detail.html', entry=entry)