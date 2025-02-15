from Site import create_app, db
from Site.config import Config

app = create_app()

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0',port=3030, debug=True)