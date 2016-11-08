import os

from flask import Blueprint, flash, redirect, render_template, request, url_for, g
from werkzeug import secure_filename
#??from app import db
from flask_login import login_required #decorator

from app import app, db
from helpers import object_list
from models import Post, Tag
from posts.forms import PostForm, ImageForm

posts = Blueprint('posts', __name__,template_folder='templates')

def post_list(template, query, **context):
    valid_statuses = (Post.STATUS_PUBLIC, Post.STATUS_DRAFT)
    query = query.filter(Post.status.in_(valid_statuses))
    if request.args.get('q'):
        search = request.args['q']
        query = query.filter(
            (Post.body.contains(search)) |
            (Post.title.contains(search)))
    return object_list(template, query, **context)

def get_post_or_404(slug, author=None):
    query = Post.query.filter(Post.slug == slug)
    if author:
        query = query.filter(Post.author == author)
    else:
        query = filter_status_by_user(query)
    return query.first_or_404()

def filter_status_by_user(query):
    if not g.user.is_authenticated:
        return query.filter(Post.status == Post.STATUS_PUBLIC)
    else:
        return query.filter(
            Post.status.in_((Post.STATUS_PUBLIC, Post.STATUS_DRAFT)))



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


# CREATE POST
#from app import db
@posts.route('/create/', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        form = PostForm(request.form)
        if form.validate():
            post = form.save_post(Post(author=g.user))
            db.session.add(post)
            db.session.commit()
            flash('Post "%s" created successfully.' % post.title, 'success')
            return redirect(url_for('posts.detail', slug=post.slug))
    else:
        form = PostForm()
    return render_template('posts/create.html', form=form)


# DETAIL VIEW / display post
@posts.route('/<slug>/')
def detail(slug):
    post = get_post_or_404(slug)
    return render_template('posts/detail.html', post=post)


# EDIT POST
@posts.route('/<slug>/edit/', methods=['GET', 'POST'])
@login_required
def edit(slug):
    post = get_post_or_404(slug, author=None)
    #post = Post.query.filter(Post.slug == slug).first_or_404()
    if request.method == 'POST':
        form = PostForm(request.form, obj=post)
        if form.validate():
            post = form.save_post(post)
            db.session.add(post)
            db.session.commit()
            return redirect(url_for('posts.detail', slug=post.slug))
    else:
        form = PostForm(obj=post)
    return render_template('posts/edit.html', post=post, form=form)

# DELETE POST
@posts.route('/<slug>/delete/', methods=['GET', 'POST'])
@login_required
def delete(slug):
    post = get_post_or_404(slug, author=None)
    if request.method == 'POST':
        post.status = Post.STATUS_DELETED
        db.session.add(post)
        db.session.commit()
        flash('Post "%s" has been deleted.' % post.title, 'success')
        return redirect(url_for('posts.index'))
    return render_template('posts/delete.html', post=post)

# IMAGES
@posts.route('/image-upload/', methods=['GET', 'POST'])
@login_required
def image_upload():
    if request.method == 'POST':
        form = ImageForm(request.form)
        if form.validate():
            image_file = request.files['file']
            filename = os.path.join(app.config['IMAGES_DIR'], secure_filename(image_file.filename))
            image_file.save(filename)
            flash('Saved %s' % os.path.basename(filename), 'success')
            return redirect(url_for('posts.index'))
    else:
        form = ImageForm()
    return render_template('posts/image_upload.html', form=form)