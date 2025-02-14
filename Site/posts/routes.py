from flask import Blueprint, redirect, url_for, render_template, request, flash, abort
from flask_login import current_user, login_required
from Site.models import Post, Comment, Picture
from Site.posts.forms import PostForm
from Site.comments.forms import CommentForm
from Site.posts.utils import save_post_picture
from Site import db
from flask_wtf.file import FileField, FileAllowed

posts = Blueprint('posts', __name__)

@posts.route('/post/<int:post_id>', methods=['GET', 'POST'])
def post(post_id):
    post = Post.query.get_or_404(post_id)
    pics = Picture.query.filter_by(post_id=post.id)
    comments = Comment.query.order_by(Comment.date_commented.desc()).filter_by(post_id=post.id).all()
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(content=form.content.data, author=current_user, post=post)
        db.session.add(comment)
        db.session.commit()
        flash("Your comment has been posted", 'success')
        return redirect(url_for("posts.post", post_id=post.id))
    return render_template('post.html', title=post.title, post=post, comments=comments, pics=pics, form=form)

@posts.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post:Post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        pic1:Picture = Picture(post_id=post.id)
        pic2:Picture = Picture(post_id=post.id)


        if form.picture0.data:
            pic1.picture=save_post_picture(form.picture0.data)
        if form.picture1.data:
            pic2.picture=save_post_picture(form.picture1.data)

        db.session.add(pic1)
        db.session.add(pic2)
        db.session.commit()
        flash("Your post has been created", 'success')
        return redirect(url_for("main.home"))
    return render_template('create_post.html', title='New Post', form=form, legend="New Post")

@posts.route('/post/<int:post_id>/update', methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        post.is_updated = True
        db.session.commit()
        flash('Your post has been updated', 'success')
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method == 'GET':
            form.title.data = post.title
            form.content.data = post.content

    return render_template('create_post.html', title='Update Post', form=form, legend="Update Postd")


@posts.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted', 'info') 
    return redirect(url_for('main.home'))