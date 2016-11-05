from flask import Blueprint
from models import Entry, Tag

posts = Blueprint('posts', __name__,template_folder='templates')

@posts.route('/')
def index():
    return 'posts index'

@posts.route('/tags/')
def tag_index():
    pass

@posts.route('/tags/<slug>/')
def tag_detail(slug):
    pass

@posts.route('/<slug>/')
def detail(slug):
    pass