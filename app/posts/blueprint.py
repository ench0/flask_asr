from flask import Blueprint
from flask import render_template

from flask import request

#??from app import db

from helpers import object_list
from models import Post, Tag
from posts.forms import PostForm

posts = Blueprint('posts', __name__,template_folder='templates')

def post_list(template, query, **context):
    search = request.args.get('q')
    if search:
        query = query.filter(
        (Post.body.contains(search)) |
        (Post.title.contains(search)))
    return object_list(template, query, **context)


@posts.route('/')
def index():
    posts = Post.query.order_by(Post.created_timestamp.desc())
    return post_list('posts/index.html', posts)

@posts.route('/tags/')
def tag_index():
    tags = Tag.query.order_by(Tag.name)
    return object_list('posts/tag_index.html', tags)

@posts.route('/tags/<slug>/')
def tag_detail(slug):
    tag = Tag.query.filter(Tag.slug == slug).first_or_404()
    posts = tag.posts.order_by(Post.created_timestamp.desc())
    return object_list('posts/tag_detail.html', posts, tag=tag)

@posts.route('/create/')
def create():
form = PostForm()
return render_template('posts/create.html', form=form)

@posts.route('/<slug>/')
def detail(slug):
    post = Post.query.filter(Post.slug == slug).first_or_404()
    return render_template('posts/detail.html', post=post)
