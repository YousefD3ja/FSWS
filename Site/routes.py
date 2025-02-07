from flask import redirect, url_for, render_template, request, flash
from Site.forms import RegistrationForm, LoginForm
from Site.models import User, Post
from Site import app, db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required

@app.route("/")
def index():
    return redirect(url_for('home'))

@app.route("/home")
def home():
    return render_template("index.html", title='Home')


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


@app.route("/user", methods=["GET", "POST"])
def user():
    pass
    #email = None
    # if "user" in session:
    #     user = session["user"]

    #     if request.method == "POST":
    #         email = request.form["email"]
    #         session["email"] = email
    #         flash("email was saved", "info")
    #     else:
    #         if "email" in session:
    #             email = session["email"]
    #     return render_template("user.html", email=email)
    # else:
    #     flash("you are not logged in", "info")
    #     return redirect(url_for("login"))

@app.route("/logout")
def logout():
    logout_user()
    flash("you have been logged out", "info")
    return redirect(url_for("login"))

@app.route("/account")
@login_required
def account():
    return render_template('account.html', title='Account')