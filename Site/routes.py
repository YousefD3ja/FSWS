import secrets, os
from PIL import Image
from flask import redirect, url_for, render_template, request, flash, abort
from Site.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm, RequestResetForm, ResetPasswordForm, CommentForm
from Site.models import User, Post, Comment
from Site import app, db, bcrypt, mail, Message, env_var
from flask_login import login_user, current_user, logout_user, login_required

@app.route("/")
def index():
    return redirect(url_for('home'))

@app.route("/home", methods=["GET", "POST"])
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=2)
    return render_template("home.html", title='Home', posts=posts)

@app.route('/register', methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()

    if form.validate_on_submit():
        hashed_pwd = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_pwd)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash(f'account created for {form.username.data}! please login', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash(f'login unsuccessfull. check email and password', 'danger')
    return render_template('login.html', title='login', form=form)


@app.route("/user/<string:username>", methods=["GET", "POST"])
def user(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404("User not found")
    posts = Post.query.filter_by(author=user).order_by(Post.date_posted.desc()).paginate(page=page, per_page=3)
    return render_template('user.html', posts=posts, user=user)

@app.route("/logout")
def logout():
    logout_user()
    flash("you have been logged out", "info")
    return redirect(url_for("login"))

###################################################################################
def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated', 'success')
        return redirect(url_for("account"))
    elif request.method == 'GET':
        if form.username.data != current_user.username:
            form.username.data = current_user.username
        if form.email.data != current_user.email:
            form.email.data = current_user.email
    return render_template('account.html', title='Account', form=form)

@app.route("/account/<int:user_id>/delete", methods=['POST'])
@login_required
def delete_account(user_id):
    user = User.query.get(user_id)
    if user != current_user:
        abort(403)
    logout_user()
    db.session.delete(user)
    db.session.commit()
    flash('Your accocunt has been deleted', 'info') 
    return redirect(url_for('home'))


####################################################################
@app.route('/post/<int:post_id>', methods=['GET', 'POST'])
def post(post_id):
    post = Post.query.get_or_404(post_id)
    comments = Comment.query.filter_by(post_id=post.id).all()
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(content=form.content.data, author=current_user, post=post)
        db.session.add(comment)
        db.session.commit()
        flash("Your comment has been posted", 'success')
        return redirect(url_for("post", post_id=post.id))
    return render_template('post.html', title=post.title, post=post, comments=comments, form=form)

@app.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash("Your post has been created", 'success')
        return redirect(url_for("home"))
    return render_template('create_post.html', title='New Post', form=form, legend="New Post")

@app.route('/post/<int:post_id>/update', methods=['GET', 'POST'])
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
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
            form.title.data = post.title
            form.content.data = post.content

    return render_template('create_post.html', title='Update Post', form=form, legend="Update Postd")


@app.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted', 'info') 
    return redirect(url_for('home'))

################
@app.route('/post/<int:post_id>/<int:comment_id>/update', methods=['GET', 'POST'])
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
        return redirect(url_for('post', post_id=post_id))
    elif request.method == 'GET':
            form.content.data = comment.content

    return render_template('edit_comment.html', title='Edit Comment', form=form, legend="Edit Comment")

@app.route('/post/<int:post_id>/<int:comment_id>/delete', methods=['POST'])
@login_required
def delete_comment(post_id, comment_id):
    comment = Comment.query.get_or_404(comment_id)
    
    if comment.author != current_user or comment.post.id != post_id:
        abort(403)
    db.session.delete(comment)
    db.session.commit()
    flash('Your comment has been deleted', 'info') 
    return redirect(url_for('post', post_id=post_id))




def send_reset_email(user:User):
    try:
        token = user.get_reset_token()
        msg = Message('Password reset', recipients=[user.email])

        msg.body = f''' to reset you'r password visit the following link:
{url_for('reset_password', token=token, _external=True)}
    
If you did not make this request then simply ignore this email
    '''
        mail.send(msg)
    except Exception as e:
        flash(f"Error sending email: {str(e)}", 'danger')
        return redirect(url_for('login'))


@app.route('/reset_password', methods=['GET','POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        #send_reset_email(user)
        #flash('An email has been sent to reset passowrd.', 'info')
        flash(f"unable to send an email", 'info')
        return redirect(url_for('login'))
    flash(f"unable to send email", 'info')
    return render_template('reset_request.html', title='Reset Password', form=form, legend='Reset Password Request')

@app.route('/reset_password/<token>', methods=['GET','POST'])
def reset_password(token):
    user = User.verify_reset_token(token)
    if not user:
        flash('invalid or expired token', 'warning')
        return redirect(url_for('reset_request'))
    
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_pwd = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_pwd
        db.session.commit()
        flash(f"You'r password has been updated", 'success')
        return redirect(url_for('home'))
    flash(f"unable to send an email", 'info')
    return render_template('reset_password.html', title='Reset Password', form=form, legend='Reset Password')

@app.route('/user/<string:username>/reset_password', methods=['GET','POST'])
@login_required
def user_pwd_reset(username):
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_pwd = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        current_user.password = hashed_pwd
        db.session.commit()
        flash(f"You'r password has been updated", 'success')
        return redirect(url_for('home'))
    return render_template('reset_password.html', title='Reset Password', form=form, legend='Reset Password')