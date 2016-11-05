from flask import Blueprint

from helpers import object_list
from models import Entry, Tag

posts = Blueprint('posts', __name__,template_folder='templates')

@posts.route('/')
def index():
    posts = Post.query.order_by(Post.created_timestamp.desc())
    return object_list('posts/index.html', posts)

@posts.route('/tags/')
def tag_index():
    pass

@posts.route('/tags/<slug>/')
def tag_detail(slug):
    pass

@posts.route('/<slug>/')
def detail(slug):
    pass