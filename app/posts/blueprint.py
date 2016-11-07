from flask import Blueprint, flash, redirect, render_template, request, url_for

#??from app import db

from helpers import object_list
from models import Post, Tag
from posts.forms import PostForm

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

def get_post_or_404(slug):
    valid_statuses = (Post.STATUS_PUBLIC, Post.STATUS_DRAFT) (Post.query.filter(
        (Post.slug == slug) & (Post.status.in_(valid_statuses))).first_or_404())


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

#create post
from app import db
@posts.route('/create/', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        form = PostForm(request.form)
        if form.validate():
            post = form.save_post(Post())
            db.session.add(post)
            db.session.commit()
            flash('Post "%s" created successfully.' % post.title, 'success')
            return redirect(url_for('posts.detail', slug=post.slug))
    else:
        form = PostForm()
    return render_template('posts/create.html', form=form)

# display post / detail view
@posts.route('/<slug>/')
def detail(slug):
    post = get_post_or_404(slug)
    return render_template('posts/detail.html', post=post)

# edit post
@posts.route('/<slug>/edit/', methods=['GET', 'POST'])
def edit(slug):
    post = get_post_or_404(slug)
    if request.method == 'POST':
        form = PostForm(request.form, obj=post)
        if form.validate():
            post = form.save_post(post)
            db.session.add(post)
            db.session.commit()
            flash('Post "%s" has been saved.' % post.title, 'success')
            return redirect(url_for('posts.detail', slug=post.slug))
    else:
        form = PostForm(obj=post)
    return render_template('posts/edit.html', post=post)

# delete post
@posts.route('/<slug>/delete/', methods=['GET', 'POST'])
def delete(slug):
    post = get_post_or_404(slug)
    if request.method == 'POST':
        post.status = Post.STATUS_DELETED
        db.session.add(post)
        db.session.commit()
        flash('Post "%s" has been deleted.' % post.title, 'success')
        return redirect(url_for('posts.index'))
    return render_template('posts/delete.html', post=post)