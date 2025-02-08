from Site import app, db
from Site.models import User, Post
from test import testing
import os

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        testing()
    app.run(host='0.0.0.0',port=3030, debug=True)