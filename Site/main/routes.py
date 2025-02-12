from flask import Blueprint, redirect, url_for, render_template, request
from Site.models import Post, User

main = Blueprint('main', __name__)

@main.route("/")
def index():
    return redirect(url_for('main.home'))

@main.route("/home", methods=["GET", "POST"])
def home():
    users = User.query(User.username)
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=2)
    return render_template("home.html", title='Home', posts=posts, users=users)