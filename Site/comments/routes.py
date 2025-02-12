from flask import Blueprint,redirect, url_for, render_template, request, flash, abort
from Site.comments.forms import (CommentForm)
from Site.models import Comment
from Site import db
from flask_login import current_user, login_required

comments = Blueprint('comments', __name__)

@comments.route('/post/<int:post_id>/<int:comment_id>/update', methods=['GET', 'POST'])
@login_required
def update_comment(post_id,comment_id):
    comment = Comment.query.get_or_404(comment_id)
    if comment.author != current_user:
        abort(403)
    form = CommentForm()
    if form.validate_on_submit():
        comment.content = form.content.data
        comment.is_updated = True
        db.session.commit()
        flash('Your comment has been updated', 'success')
        return redirect(url_for('posts.post', post_id=post_id))
    elif request.method == 'GET':
            form.content.data = comment.content

    return render_template('edit_comment.html', title='Edit Comment', form=form, legend="Edit Comment")

@comments.route('/post/<int:post_id>/<int:comment_id>/delete', methods=['POST'])
@login_required
def delete_comment(post_id, comment_id):
    comment = Comment.query.get_or_404(comment_id)
    
    if comment.author != current_user or comment.post.id != post_id:
        abort(403)
    db.session.delete(comment)
    db.session.commit()
    flash('Your comment has been deleted', 'info') 
    return redirect(url_for('posts.post', post_id=post_id))