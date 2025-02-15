from flask import Blueprint, redirect, url_for, render_template, request, flash, abort, Response
from flask_login import current_user, login_required, login_user, logout_user
from Site import db, bcrypt
from Site.models import User, Post
from Site.users.forms import RegistrationForm, LoginForm, UpdateAccountForm, RequestResetForm, ResetPasswordForm 
from Site.users.utils import save_picture
from flask import jsonify, make_response
import json

users = Blueprint('users', __name__)

@users.route('/getusers', methods=["POST"])
def get_users():

    if request.is_json:
        req = request.get_json()
        users = User.query.filter(User.username.icontains(req.get("user"))).all()

        users_dic = []
        #users_dic.clear()
        for user in users:
            #userArray = {f'user{user.id}': {'name': user.username, 'email': user.email, 'image': user.image_file}}
            users_dic.append({
                'id': user.id,'name': user.username, 'email': user.email,

                'image': url_for('static', filename=f'profile_pics/{user.image_file}'), 

                'userURL': url_for('users.user', username=user.username)
                })


        res = make_response(jsonify(users_dic), 200)

        return res
    else:
        res = make_response(jsonify("no json recived"), 400)
        return res


@users.route('/register', methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()

    if form.validate_on_submit():
        hashed_pwd = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_pwd)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash(f'account created for {form.username.data}! please login', 'success')
        return redirect(url_for('main.home'))
    return render_template('register.html', title='Register', form=form)

@users.route('/login', methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash(f'login unsuccessfull. check email and password', 'danger')
    return render_template('login.html', title='login', form=form)


@users.route("/user/<string:username>", methods=["GET", "POST"])
def user(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404("User not found")
    posts = Post.query.filter_by(author=user).order_by(Post.date_posted.desc()).paginate(page=page, per_page=3)
    return render_template('user.html', posts=posts, user=user)

@users.route("/logout")
def logout():
    logout_user()
    flash("you have been logged out", "info")
    return redirect(url_for("users.login"))

###################################################################################



@users.route("/account", methods=['GET', 'POST'])
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
        return redirect(url_for("users.account"))
    elif request.method == 'GET':
        if form.username.data != current_user.username:
            form.username.data = current_user.username
        if form.email.data != current_user.email:
            form.email.data = current_user.email
    return render_template('account.html', title='Account', form=form)

@users.route("/account/<int:user_id>/delete", methods=['POST'])
@login_required
def delete_account(user_id):
    user = User.query.get(user_id)
    if user != current_user:
        abort(403)
    logout_user()
    db.session.delete(user)
    db.session.commit()
    flash('Your accocunt has been deleted', 'info') 
    return redirect(url_for('main.home'))

@users.route('/reset_password', methods=['GET','POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        #send_reset_email(user)
        #flash('An email has been sent to reset passowrd.', 'info')
        flash(f"unable to send an email", 'info')
        return redirect(url_for('users.login'))
    flash(f"unable to send email", 'info')
    return render_template('reset_request.html', title='Reset Password', form=form, legend='Reset Password Request')

@users.route('/reset_password/<token>', methods=['GET','POST'])
def reset_password(token):
    user = User.verify_reset_token(token)
    if not user:
        flash('invalid or expired token', 'warning')
        return redirect(url_for('users.reset_request'))
    
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_pwd = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_pwd
        db.session.commit()
        flash(f"You'r password has been updated", 'success')
        return redirect(url_for('main.home'))
    flash(f"unable to send an email", 'info')
    return render_template('reset_password.html', title='Reset Password', form=form, legend='Reset Password')

@users.route('/user/<string:username>/reset_password', methods=['GET','POST'])
@login_required
def user_pwd_reset(username):
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_pwd = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        current_user.password = hashed_pwd
        db.session.commit()
        flash(f"You'r password has been updated", 'success')
        return redirect(url_for('main.home'))
    return render_template('reset_password.html', title='Reset Password', form=form, legend='Reset Password')