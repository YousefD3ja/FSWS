import secrets, os
from PIL import Image
from flask import redirect, url_for, render_template, request, flash
from Site.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm
from Site.models import User, Post
from Site import app, db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required

@app.route("/")
def index():
    return redirect(url_for('home'))

@app.route("/home")
def home():
    posts = Post.query.all()
    img_file = None
    if current_user.is_authenticated:
        img_file = url_for('static', filename=f'profile_pics/{current_user.image_file}')
    return render_template("home.html", title='Home', image_file=img_file, posts=posts)


# @app.route("/login", methods=["POST", "GET"])
# def login():
#     if request.method == "POST":
#         session.permanent = True
#         user = request.form["nm"]
#         session["user"] = user
#         flash("you have been logged in successfully", "info")
#         return redirect(url_for("user"))
#     else:
#         if "user" in session:
#             flash("you are already logged in", "info")
#             return redirect(url_for("user"))
#         else:
#             return render_template("login.html", Title='Login')

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
        flash(f'account created for {form.username.data}! please login', 'success')
        return redirect(url_for('login'))
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


# @app.route("/user", methods=["GET", "POST"])
# def user():
    # email = None
    #  if "user" in session:
    #      user = session["user"]

    #      if request.method == "POST":
    #          email = request.form["email"]
    #          session["email"] = email
    #          flash("email was saved", "info")
    #      else:
    #          if "email" in session:
    #              email = session["email"]
    #      return render_template("user.html", email=email)
    #  else:
    #      flash("you are not logged in", "info")
    #      return redirect(url_for("login"))

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
    img_file = url_for('static', filename=f'profile_pics/{current_user.image_file}')
    return render_template('account.html', title='Account', image_file=img_file, form=form)

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
    img_file = url_for('static', filename=f'profile_pics/{current_user.image_file}')
    return render_template('create_post.html', title='New Post', form=form, image_file=img_file)