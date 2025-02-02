from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta
from forms import RegistrationForm, LoginForm
from flask_sqlalchemy import SQLAlchemy
import email_validator


app = Flask(__name__)
app.secret_key = "Y0u$@f"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.permanent_session_lifetime = timedelta(minutes=10)

db = SQLAlchemy(app)

class users(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(100))

    def __init__(self, name, email):
        self.name = name
        self.email = email

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
    form = RegistrationForm()

    if form.validate_on_submit():
        flash(f'account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@yousef.com' and form.password.data == '123456789':
            flash(f'welcome back admin!', 'success')
            return redirect(url_for('home'))
        else:
            flash(f'login unsuccessfull!', 'danger')
    return render_template('login.html', title='login', form=form)


@app.route("/user", methods=["GET", "POST"])
def user():
    email = None
    if "user" in session:
        user = session["user"]

        if request.method == "POST":
            email = request.form["email"]
            session["email"] = email
            flash("email was saved", "info")
        else:
            if "email" in session:
                email = session["email"]
        return render_template("user.html", email=email)
    else:
        flash("you are not logged in", "info")
        return redirect(url_for("login"))

@app.route("/logout")
def logout():
    flash("you have been logged out", "info")
    session.pop("user", None)
    session.pop("email", None)
    return redirect(url_for("login"))




if __name__ == "__main__":
    #db.create_all()
    app.run(host='0.0.0.0',port=3030, debug=True)